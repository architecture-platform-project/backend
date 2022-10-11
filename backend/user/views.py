from rest_framework import generics, status
from rest_framework.response import Response

from user.serializers import EmailUniqueCheckSerializer


# Todo: blacklist API


class EmailUniqueCheck(generics.CreateAPIView):
    """
    이메일 중복 확인 API
    """

    serializer_class = EmailUniqueCheckSerializer

    def post(self, request, *args, **kwargs):
        """
        이메일 중복확인
        :param request: email
        :return:
        """
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            return Response(
                data={"detail": ["You can use this email"]}, status=status.HTTP_200_OK
            )
        else:
            detail = dict()
            detail["detail"] = serializer.errors["email"]
            return Response(data=detail, status=status.HTTP_400_BAD_REQUEST)
