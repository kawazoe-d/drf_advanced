from rest_framework.views import APIView
from rest_framework.response import Response

from common.serializers import UserSerializer
from core.models import User

class AmbassadorAPIView(APIView):
    """
    アンバサダー取得APIクラス
    response
    [
        {
            "id": 1,
            "first_name": "admin",
            "last_name": "admin",
            "email": "admin@a.com",
            "is_ambassador": true
        },
        {
            "id": 2,
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com",
            "is_ambassador": true
        }
    ]
    """
    def get(self, _):
        ambassadors = User.objects.filter(is_ambassador=True)
        # リスト形式のjsonを出力する場合は、キーワード引数にmany=Trueを指定する
        serializer = UserSerializer(ambassadors, many=True)
        return Response(serializer.data)