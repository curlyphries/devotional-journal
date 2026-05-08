use aes_gcm::{
    aead::{Aead, KeyInit},
    Aes256Gcm, Nonce,
};
use anyhow::{anyhow, Result};
use hkdf::Hkdf;
use keyring::Entry;
use rand::RngCore;
use sha2::Sha256;

const KEYRING_SERVICE: &str = "com.curlyphries.devotional";
const KEYRING_USER: &str = "encryption_root";

/// Get or create encryption root key from OS keychain
pub fn get_or_create_root_key() -> Result<[u8; 32]> {
    let entry = Entry::new(KEYRING_SERVICE, KEYRING_USER)?;
    
    match entry.get_password() {
        Ok(base64_key) => {
            let key = base64::decode(base64_key)?;
            if key.len() != 32 {
                return Err(anyhow!("Invalid key length in keychain"));
            }
            let mut arr = [0u8; 32];
            arr.copy_from_slice(&key);
            Ok(arr)
        }
        Err(_) => {
            // Generate new key
            let mut key = [0u8; 32];
            rand::thread_rng().fill_bytes(&mut key);
            let base64_key = base64::encode(&key);
            entry.set_password(&base64_key)?;
            Ok(key)
        }
    }
}

/// Derive data encryption key from root key using HKDF
pub fn derive_data_key(root_key: &[u8; 32], context: &str) -> Result<[u8; 32]> {
    let hkdf = Hkdf::<Sha256>::from_prk(root_key)
        .map_err(|_| anyhow!("Invalid PRK for HKDF"))?;
    
    let mut okm = [0u8; 32];
    hkdf.expand(context.as_bytes(), &mut okm)
        .map_err(|_| anyhow!("HKDF expand failed"))?;
    
    Ok(okm)
}

/// Encrypt plaintext with AES-256-GCM
pub fn encrypt(plaintext: &[u8], key: &[u8; 32]) -> Result<Vec<u8>> {
    let cipher = Aes256Gcm::new_from_slice(key)?;
    
    let mut nonce_bytes = [0u8; 12];
    rand::thread_rng().fill_bytes(&mut nonce_bytes);
    let nonce = Nonce::from_slice(&nonce_bytes);
    
    let ciphertext = cipher
        .encrypt(nonce, plaintext)
        .map_err(|e| anyhow!("Encryption failed: {}", e))?;
    
    // Format: [nonce (12 bytes)][ciphertext]
    let mut result = Vec::with_capacity(12 + ciphertext.len());
    result.extend_from_slice(&nonce_bytes);
    result.extend_from_slice(&ciphertext);
    
    Ok(result)
}

/// Decrypt ciphertext with AES-256-GCM
pub fn decrypt(ciphertext: &[u8], key: &[u8; 32]) -> Result<Vec<u8>> {
    if ciphertext.len() < 12 {
        return Err(anyhow!("Ciphertext too short"));
    }
    
    let cipher = Aes256Gcm::new_from_slice(key)?;
    let nonce = Nonce::from_slice(&ciphertext[..12]);
    
    let plaintext = cipher
        .decrypt(nonce, &ciphertext[12..])
        .map_err(|e| anyhow!("Decryption failed: {}", e))?;
    
    Ok(plaintext)
}

/// Encrypt with root key (convenience)
pub fn encrypt_with_root(plaintext: &[u8]) -> Result<Vec<u8>> {
    let root_key = get_or_create_root_key()?;
    let data_key = derive_data_key(&root_key, "journal_entries_v1")?;
    encrypt(plaintext, &data_key)
}

/// Decrypt with root key (convenience)
pub fn decrypt_with_root(ciphertext: &[u8]) -> Result<Vec<u8>> {
    let root_key = get_or_create_root_key()?;
    let data_key = derive_data_key(&root_key, "journal_entries_v1")?;
    decrypt(ciphertext, &data_key)
}

/// Wipe all keys (for sign out)
pub fn wipe_keys() -> Result<()> {
    let entry = Entry::new(KEYRING_SERVICE, KEYRING_USER)?;
    entry.delete_password()?;
    Ok(())
}
