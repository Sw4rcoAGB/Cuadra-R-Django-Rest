import pytest
from django.contrib.auth.hashers import make_password, check_password
from api.models import Usuario, Rol, PasswordResetToken
from api.services.auth_service import AuthService

@pytest.mark.django_db
class TestAuthService:
    @pytest.fixture(autouse=True)
    def setup_roles(self):
        self.admin_role, _ = Rol.objects.get_or_create(nombre='Admin')
        self.tutor_role, _ = Rol.objects.get_or_create(nombre='Tutor')
        
        self.user = Usuario.objects.create(
            rol=self.admin_role,
            email="test@cuadraerre.com",
            password=make_password("oldpassword123"),
            nombre_completo="Juan Perez",
            telefono="123456"
        )

    def test_update_profile_success(self):
        data = {
            "nombre_completo": "juan perez editado",
            "email": "newemail@cuadraerre.com",
            "telefono": "654321"
        }
        updated_user = AuthService.update_profile(self.user.id, data)
        assert updated_user.nombre_completo == "Juan Perez Editado"  # Should capitalize words
        assert updated_user.email == "newemail@cuadraerre.com"
        assert updated_user.telefono == "654321"

    def test_update_profile_duplicate_email(self):
        # Create another user
        Usuario.objects.create(
            rol=self.tutor_role,
            email="duplicate@cuadraerre.com",
            password=make_password("password"),
            nombre_completo="Otro Usuario"
        )
        data = {"email": "duplicate@cuadraerre.com"}
        with pytest.raises(ValueError, match="correo ya está en uso"):
            AuthService.update_profile(self.user.id, data)

    def test_change_password_success(self):
        AuthService.change_password(self.user.id, "oldpassword123", "newsecurepassword123")
        self.user.refresh_from_db()
        assert check_password("newsecurepassword123", self.user.password)

    def test_change_password_invalid_current(self):
        with pytest.raises(PermissionError, match="contraseña actual es incorrecta"):
            AuthService.change_password(self.user.id, "wrongpassword", "newpassword123")

    def test_change_password_too_short(self):
        with pytest.raises(ValueError, match="al menos 8 caracteres"):
            AuthService.change_password(self.user.id, "oldpassword123", "short")

    def test_forgot_password_success(self):
        link = AuthService.forgot_password("test@cuadraerre.com")
        assert "reset-password" in link
        token = PasswordResetToken.objects.filter(usuario=self.user, utilizado=False).first()
        assert token is not None
        assert str(token.id) in link

    def test_reset_password_magic_success(self):
        token = PasswordResetToken.objects.create(usuario=self.user)
        AuthService.reset_password_magic(str(token.id), "brandnewpassword123")
        self.user.refresh_from_db()
        assert check_password("brandnewpassword123", self.user.password)
        token.refresh_from_db()
        assert token.utilizado is True
