from rest_framework.views import APIView


class VideoListView(APIView):
    def get(self, request):
        pass


class VideoPlaylistView(APIView):
    def get(self, request, movie_id, resolution):
        pass


class VideoSegmentView(APIView):
    def get(self, request, movie_id, resolution, segment):
        pass
