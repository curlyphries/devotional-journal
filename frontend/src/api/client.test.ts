import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import axios, { AxiosError, AxiosHeaders, type AxiosResponse, type InternalAxiosRequestConfig } from 'axios'
import client, { DEFAULT_TIMEOUT_MS } from './client'

const store = new Map<string, string>()

function respond(config: InternalAxiosRequestConfig, status: number, data: unknown): Promise<AxiosResponse> {
  const response = { status, data, headers: new AxiosHeaders(), statusText: '', config } as AxiosResponse
  if (status >= 400) {
    return Promise.reject(new AxiosError('Request failed', AxiosError.ERR_BAD_RESPONSE, config, {}, response))
  }
  return Promise.resolve(response)
}

describe('api client', () => {
  const originalAdapter = client.defaults.adapter

  beforeEach(() => {
    store.clear()
    vi.mocked(localStorage.getItem).mockImplementation((key: string) => store.get(key) ?? null)
    vi.mocked(localStorage.setItem).mockImplementation((key: string, value: string) => void store.set(key, value))
    vi.mocked(localStorage.removeItem).mockImplementation((key: string) => void store.delete(key))
  })

  afterEach(() => {
    client.defaults.adapter = originalAdapter
    vi.restoreAllMocks()
  })

  it('has a 30s default timeout that a request can override', async () => {
    expect(DEFAULT_TIMEOUT_MS).toBe(30_000)
    const seen: (number | undefined)[] = []
    client.defaults.adapter = (config) => {
      seen.push(config.timeout)
      return respond(config, 200, {})
    }

    await client.get('/a/')
    await client.post('/ai/', {}, { timeout: 120_000 })

    expect(seen).toEqual([30_000, 120_000])
  })

  it('refreshes once for concurrent 401s and retries each request with the new token', async () => {
    store.set('access_token', 'old')
    store.set('refresh_token', 'refresh-1')
    const refresh = vi.spyOn(axios, 'post').mockImplementation(async () => {
      await new Promise((resolve) => setTimeout(resolve, 10))
      return { data: { access_token: 'new', refresh_token: 'refresh-2' } }
    })
    client.defaults.adapter = (config) =>
      config.headers.Authorization === 'Bearer new'
        ? respond(config, 200, { url: config.url })
        : respond(config, 401, { error: 'expired', code: 'NOT_AUTHENTICATED' })

    const results = await Promise.all([client.get('/one/'), client.get('/two/'), client.get('/three/')])

    expect(refresh).toHaveBeenCalledTimes(1)
    expect(refresh.mock.calls[0][1]).toEqual({ refresh_token: 'refresh-1' })
    expect(results.map((r) => r.data.url)).toEqual(['/one/', '/two/', '/three/'])
    expect(store.get('access_token')).toBe('new')
    expect(store.get('refresh_token')).toBe('refresh-2')
  })

  it('clears the tokens and rejects with the original error when the refresh fails', async () => {
    store.set('access_token', 'old')
    store.set('refresh_token', 'refresh-1')
    vi.spyOn(axios, 'post').mockRejectedValue(new Error('refresh rejected'))
    client.defaults.adapter = (config) => respond(config, 401, { error: 'expired', code: 'NOT_AUTHENTICATED' })

    const error = await client.get('/one/').catch((err) => err)

    expect(axios.isAxiosError(error)).toBe(true)
    expect(error.response.status).toBe(401)
    expect(store.has('access_token')).toBe(false)
    expect(store.has('refresh_token')).toBe(false)
  })

  it('clears the tokens without calling refresh when there is no refresh token', async () => {
    store.set('access_token', 'old')
    const refresh = vi.spyOn(axios, 'post')
    client.defaults.adapter = (config) => respond(config, 401, {})

    await expect(client.get('/one/')).rejects.toMatchObject({ response: { status: 401 } })

    expect(refresh).not.toHaveBeenCalled()
    expect(store.has('access_token')).toBe(false)
  })

  it('does not treat a failed sign-in as an expired session', async () => {
    store.set('refresh_token', 'refresh-1')
    const refresh = vi.spyOn(axios, 'post')
    client.defaults.adapter = (config) => respond(config, 401, { error: 'Invalid link' })

    await expect(client.post('/auth/magic-link/verify/', { token: 'x' })).rejects.toBeTruthy()

    expect(refresh).not.toHaveBeenCalled()
    expect(store.get('refresh_token')).toBe('refresh-1')
  })
})
