from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.utils import timezone
import datetime
from api.models import Usuario, PasswordResetToken, BitacoraSeguridad

class AuthService:
    @staticmethod
    def change_password(usuario_id, current_password, new_password, ip_address=None):
        if not current_password or not new_password:
            raise ValueError("Contraseña actual y nueva son requeridas.")
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            raise ValueError("Usuario no encontrado.")

        if not check_password(current_password, usuario.password):
            raise PermissionError("La contraseña actual es incorrecta.")

        if len(new_password) < 8:
            raise ValueError("La nueva contraseña debe tener al menos 8 caracteres.")

        usuario.password = make_password(new_password)
        usuario.save()

        # Log event
        BitacoraSeguridad.objects.create(
            usuario_afectado=usuario,
            usuario_accion=usuario,
            tipo_evento='PASSWORD_CHANGE',
            descripcion=f"Cambio de contraseña exitoso para el usuario {usuario.email}.",
            ip_address=ip_address
        )
        return usuario

    @staticmethod
    def forgot_password(email):
        email = email.strip()
        if not email:
            raise ValueError("El correo es requerido.")

        try:
            usuario = Usuario.objects.get(email__iexact=email)
        except Usuario.DoesNotExist:
            raise ValueError("Este correo no está registrado en el sistema. Verifica que esté bien escrito.")

        # Invalida tokens anteriores para que solo el último funcione
        PasswordResetToken.objects.filter(usuario=usuario, utilizado=False).update(utilizado=True)
        
        # Create token
        token = PasswordResetToken.objects.create(usuario=usuario)
        reset_link = f"http://localhost:3000/reset-password?token={token.id}"
        
        # Enviar correo de forma asíncrona
        import threading
        def enviar_correo_magico():
            from django.core.mail import send_mail
            from django.conf import settings
            
            html_message = f"""
            <div style="font-family: Arial, sans-serif; padding: 20px; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #821026;">Recuperación de Acceso</h2>
                <p>Hola <strong>{usuario.nombre_completo}</strong>,</p>
                <p>Hemos recibido una solicitud para acceder a tu cuenta en el Portal de Cuadra Erre.</p>
                <p>Haz clic en el siguiente botón seguro para establecer tu nueva contraseña:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_link}" style="background-color: #821026; color: white; padding: 15px 25px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
                        Reestablecer Contraseña
                    </a>
                </div>
                <p style="color: #666; font-size: 12px;">Este enlace expira en 1 hora. Si solicitas otro, este enlace quedará invalidado de inmediato.</p>
            </div>
            """
            try:
                send_mail(
                    subject="🔑 Recupera tu acceso a Cuadra Erre",
                    message=f"Entra a este enlace para recuperar tu contraseña: {reset_link}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[usuario.email],
                    fail_silently=True,
                    html_message=html_message
                )
            except Exception as e:
                print("Error al enviar correo:", e)

        threading.Thread(target=enviar_correo_magico).start()
        return reset_link

    @staticmethod
    def reset_password_magic(token_id, new_password):
        if not token_id or not new_password:
            raise ValueError("Token y nueva contraseña son requeridos.")
            
        try:
            token_obj = PasswordResetToken.objects.get(id=token_id)
        except PasswordResetToken.DoesNotExist:
            raise ValueError("Token inválido.")

        if not token_obj.is_valid():
            raise ValueError("El enlace ha expirado o ya fue utilizado.")
            
        usuario = token_obj.usuario
        usuario.password = make_password(new_password)
        usuario.save()
        
        token_obj.utilizado = True
        token_obj.save()
        return usuario

    @staticmethod
    def resetear_password(usuario_id, nueva_password):
        if not nueva_password:
            raise ValueError("Debe proporcionar una nueva contraseña.")

        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            raise ValueError("Usuario no encontrado.")

        usuario.password = make_password(nueva_password)
        usuario.save()
        return usuario

    @staticmethod
    def update_profile(usuario_id, data):
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            raise ValueError("Usuario no encontrado.")

        if data.get('nombre_completo'):
            from api.common.utils import cap
            usuario.nombre_completo = cap(data['nombre_completo'])
        if data.get('email'):
            existing = Usuario.objects.filter(email=data['email']).exclude(id=usuario_id).first()
            if existing:
                raise ValueError("Este correo ya está en uso.")
            usuario.email = data['email']
        if data.get('telefono'):
            usuario.telefono = data['telefono']
        usuario.save()
        return usuario
