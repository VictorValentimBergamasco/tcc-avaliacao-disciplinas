from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from .permissions import IsAdminRole


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class ChangePasswordView(APIView):
    """Permite que o usuário logado defina/troque a própria senha.

    Usado no fluxo de primeiro login do professor: a senha provisória
    cadastrada pelo admin força must_change_password=True, e essa view
    finaliza a troca e desmarca a flag.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        current_password = serializer.validated_data.get("current_password", "")
        new_password = serializer.validated_data["new_password"]

        # Se o usuário NÃO está no fluxo de primeiro login, exigimos a senha atual.
        if not user.must_change_password:
            if not current_password or not user.check_password(current_password):
                return Response(
                    {"detail": "Senha atual incorreta."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        user.set_password(new_password)
        user.must_change_password = False
        user.save(update_fields=["password", "must_change_password"])

        return Response(
            {"detail": "Senha alterada com sucesso.", "must_change_password": False},
            status=status.HTTP_200_OK,
        )


class PasswordResetRequestView(APIView):
    """Recebe um e-mail e, se existir um usuario ativo com ele, envia um
    link de redefinicao por e-mail.

    Por seguranca a resposta e sempre 200 (nao revela se o e-mail existe).
    Em desenvolvimento, o backend de e-mail e o console - o link aparece
    no terminal do runserver.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["institutional_email"]

        user = User.objects.filter(institutional_email__iexact=email, is_active=True).first()

        if user is not None:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            link = f"{settings.FRONTEND_URL.rstrip('/')}/reset-password/{uid}/{token}"

            assunto = "Recuperacao de senha - Sistema de Avaliacao FT-UNICAMP"
            corpo = (
                f"Ola, {user.first_name or user.institutional_email}!\n\n"
                "Recebemos uma solicitacao para redefinir a sua senha do sistema "
                "de avaliacao de disciplinas da FT-UNICAMP.\n\n"
                f"Para criar uma nova senha, acesse o link abaixo:\n{link}\n\n"
                "O link e valido por algumas horas. Se voce nao solicitou essa "
                "redefinicao, basta ignorar este e-mail.\n\n"
                "Atenciosamente,\nEquipe FT-UNICAMP"
            )

            try:
                send_mail(
                    assunto,
                    corpo,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.institutional_email],
                    fail_silently=False,
                )
            except Exception:
                # Em dev nao queremos derrubar a rota se o backend de e-mail
                # estiver mal configurado. Em producao isso seria logado.
                pass

        return Response(
            {"detail": "Se o e-mail informado estiver cadastrado, enviamos um link de redefinicao."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    """Confirma a redefinicao validando uid + token e setando a nova senha."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid_b64 = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            uid = force_str(urlsafe_base64_decode(uid_b64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"detail": "Link invalido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Link invalido ou expirado. Solicite um novo."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        # A senha foi redefinida pelo proprio usuario - nao forca troca.
        user.must_change_password = False
        user.save(update_fields=["password", "must_change_password"])

        return Response(
            {"detail": "Senha redefinida com sucesso. Voce ja pode fazer login."},
            status=status.HTTP_200_OK,
        )


class ProfessorListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(role="professor").order_by("first_name", "last_name")
    permission_classes = [IsAdminRole]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer


class ProfessorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(role="professor")
    permission_classes = [IsAdminRole]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserCreateSerializer
        return UserSerializer
