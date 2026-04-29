"""
Views for Bible text retrieval.
"""
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BibleTranslation, BibleVerse
from .serializers import (
    BibleTranslationSerializer,
    BibleVerseSerializer,
    PassageRequestSerializer,
    SearchRequestSerializer,
)
from . import bolls_api
from . import text_verifier


class TranslationListView(APIView):
    permission_classes = [AllowAny]
    """
    List available Bible translations.
    """
    def get(self, request):
        translations = BibleTranslation.objects.all()
        serializer = BibleTranslationSerializer(translations, many=True)
        return Response(serializer.data)


class PassageReadView(APIView):
    permission_classes = [AllowAny]
    """
    Read a Bible passage.
    """
    def get(self, request):
        serializer = PassageRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            translation = BibleTranslation.objects.get(code=data['translation'])
        except BibleTranslation.DoesNotExist:
            return Response(
                {'error': 'Translation not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        verses = BibleVerse.objects.filter(
            translation=translation,
            book__iexact=data['book'],
            chapter=data['chapter']
        )

        if 'verse_start' in data:
            verses = verses.filter(verse__gte=data['verse_start'])
        if 'verse_end' in data:
            verses = verses.filter(verse__lte=data['verse_end'])

        verses = verses.order_by('verse')

        if not verses.exists():
            return Response(
                {'error': 'Passage not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            'translation': BibleTranslationSerializer(translation).data,
            'verses': BibleVerseSerializer(verses, many=True).data,
            'full_text': ' '.join(v.text for v in verses)
        })


class SearchView(APIView):
    permission_classes = [AllowAny]
    """
    Full-text search within a translation.
    """
    def get(self, request):
        serializer = SearchRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            translation = BibleTranslation.objects.get(code=data['translation'])
        except BibleTranslation.DoesNotExist:
            return Response(
                {'error': 'Translation not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        verses = BibleVerse.objects.filter(
            translation=translation,
            text__icontains=data['query']
        ).order_by('book', 'chapter', 'verse')[:50]

        return Response({
            'query': data['query'],
            'translation': BibleTranslationSerializer(translation).data,
            'results': BibleVerseSerializer(verses, many=True).data,
            'count': verses.count()
        })


# ============================================================
# Bolls Bible API Views (External translations)
# ============================================================

class BollsTranslationsView(APIView):
    """
    List available translations from Bolls Bible API.
    Personal use only - includes public domain and fair-use translations.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        translations = bolls_api.get_available_translations()
        return Response({
            'source': 'bolls.life',
            'note': 'Personal use only. Some translations require attribution.',
            'translations': translations
        })


class BollsPassageView(APIView):
    """
    Read a passage from Bolls Bible API.
    Supports: KJV, ASV, YLT, WEB (public domain), RVR1960 (fair use)
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        translation = request.query_params.get('translation', 'KJV')
        book = request.query_params.get('book')
        chapter = request.query_params.get('chapter')
        verse_start = request.query_params.get('verse_start')
        verse_end = request.query_params.get('verse_end')

        if not book or not chapter:
            return Response(
                {'error': 'book and chapter are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            chapter = int(chapter)
            book = bolls_api.normalize_book(book)

            if verse_start and verse_end:
                verses = bolls_api.get_verse_range(
                    translation, book, chapter,
                    int(verse_start), int(verse_end)
                )
            else:
                raw_verses = bolls_api.get_chapter(translation, book, chapter)
                verses = [
                    {
                        'verse': v.get('verse'),
                        'text': v.get('text', ''),
                        'translation': translation,
                        'book': book,
                        'chapter': chapter,
                    }
                    for v in raw_verses
                ]

            # Get attribution if needed
            trans_info = bolls_api.ALLOWED_TRANSLATIONS.get(translation, {})
            attribution = trans_info.get('attribution')

            return Response({
                'source': 'bolls.life',
                'translation': {
                    'code': translation,
                    'name': trans_info.get('name', translation),
                    'language': trans_info.get('language', 'en'),
                },
                'book': book,
                'chapter': chapter,
                'verses': verses,
                'full_text': ' '.join(v['text'] for v in verses),
                'attribution': attribution,
            })

        except bolls_api.BollsAPIError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            return Response(
                {'error': f'Invalid parameter: {e}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class BollsSearchView(APIView):
    """
    Search within a Bolls Bible translation.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        translation = request.query_params.get('translation', 'KJV')
        query = request.query_params.get('query', request.query_params.get('q'))
        limit = int(request.query_params.get('limit', 20))

        if not query:
            return Response(
                {'error': 'query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            results = bolls_api.search_text(translation, query, limit)
            trans_info = bolls_api.ALLOWED_TRANSLATIONS.get(translation, {})

            return Response({
                'source': 'bolls.life',
                'query': query,
                'translation': {
                    'code': translation,
                    'name': trans_info.get('name', translation),
                },
                'results': results,
                'count': len(results),
                'attribution': trans_info.get('attribution'),
            })

        except bolls_api.BollsAPIError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class BollsVerifyView(APIView):
    """
    Verify Bible text integrity against trusted sources.
    Cross-references Bolls API text with:
    - Local KJV database (31,100 verified verses)
    - bible-api.com (World English Bible - public domain)
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        translation = request.query_params.get('translation', 'KJV')
        book = request.query_params.get('book')
        chapter = request.query_params.get('chapter')
        verse = request.query_params.get('verse')
        
        if not book or not chapter:
            return Response(
                {'error': 'book and chapter are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            chapter_num = int(chapter)
            book_code = bolls_api.normalize_book(book)
            
            # Fetch from Bolls
            raw_verses = bolls_api.get_chapter(translation, book_code, chapter_num)
            
            if verse:
                # Verify single verse
                verse_num = int(verse)
                verse_data = next(
                    (v for v in raw_verses if v.get('verse') == verse_num),
                    None
                )
                
                if not verse_data:
                    return Response(
                        {'error': f'Verse {verse_num} not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                result = text_verifier.verify_verse(
                    translation, book_code, chapter_num, verse_num,
                    verse_data.get('text', '')
                )
                
                return Response({
                    'type': 'single_verse',
                    'source': 'bolls.life',
                    **result
                })
            else:
                # Verify entire chapter
                verses = [
                    {'verse': v.get('verse'), 'text': v.get('text', '')}
                    for v in raw_verses
                ]
                
                result = text_verifier.verify_chapter(
                    translation, book_code, chapter_num, verses
                )
                
                return Response({
                    'type': 'chapter',
                    'source': 'bolls.life',
                    **result
                })
        
        except bolls_api.BollsAPIError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            return Response(
                {'error': f'Invalid parameter: {e}'},
                status=status.HTTP_400_BAD_REQUEST
            )


# Highlight views
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import VerseHighlight
from .serializers import VerseHighlightSerializer


class HighlightListCreateView(ListCreateAPIView):
    """
    List and create verse highlights for the current user.
    Uses update_or_create to handle duplicate verse highlights.
    """
    serializer_class = VerseHighlightSerializer
    pagination_class = None  # Disable pagination for highlights

    def get_queryset(self):
        queryset = VerseHighlight.objects.filter(user=self.request.user)
        
        # Filter by book/chapter if provided
        book = self.request.query_params.get('book')
        chapter = self.request.query_params.get('chapter')
        translation = self.request.query_params.get('translation')
        
        if book:
            queryset = queryset.filter(book__iexact=book)
        if chapter:
            queryset = queryset.filter(chapter=chapter)
        if translation:
            queryset = queryset.filter(translation=translation)
            
        return queryset

    def create(self, request, *args, **kwargs):
        """Override create to use update_or_create for existing highlights."""
        data = request.data
        highlight, created = VerseHighlight.objects.update_or_create(
            user=request.user,
            book=data.get('book'),
            chapter=data.get('chapter'),
            verse_start=data.get('verse_start'),
            translation=data.get('translation', 'KJV'),
            defaults={
                'verse_end': data.get('verse_end'),
                'color': data.get('color', 'yellow'),
                'note': data.get('note', ''),
            }
        )
        serializer = self.get_serializer(highlight)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)


class HighlightDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a verse highlight.
    """
    serializer_class = VerseHighlightSerializer

    def get_queryset(self):
        return VerseHighlight.objects.filter(user=self.request.user)
