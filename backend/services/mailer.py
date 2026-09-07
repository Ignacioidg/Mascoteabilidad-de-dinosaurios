# -*- coding: utf-8 -*-
"""
Servicio de Notificaciones y Correo Electrónico
DinoMascota Dashboard - Bases de Datos Aplicada (UAI)

Soporta:
1. Envío real vía SMTP (si se configuran variables de entorno SMTP_*)
2. Modo Simulación / Local (por defecto): imprime en terminal y retorna el código
   para que docentes y evaluadores puedan probar la funcionalidad offline.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Any

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", "no-reply@dinomascota.uai.edu.ar")

def is_smtp_configured() -> bool:
    return bool(SMTP_HOST and SMTP_USER and SMTP_PASSWORD)

def print_simulated_email(to_email: str, username: str, subject: str, code: str, purpose: str):
    """Imprime en la terminal una tarjeta visual del correo simulado para depuración/evaluación."""
    box_width = 72
    print("\n" + "=" * box_width)
    print(" [SISTEMA DE CORREO - DINOMASCOTA UAI]".center(box_width))
    print(" MODO: Simulacion Local (Offline / Academico)".center(box_width))
    print("-" * box_width)
    print(f" Para:      {to_email} (Usuario: {username})")
    print(f" Asunto:    {subject}")
    print(f" Proposito: {purpose}")
    print("-" * box_width)
    print(f" >>> CODIGO DE SEGURIDAD (6 DIGITOS):  [ {code} ]")
    print("     (Valido por 15 minutos)")
    print("=" * box_width + "\n")


def send_verification_email(to_email: str, username: str, code: str) -> Dict[str, Any]:
    """Envía o simula el correo con el código de verificación para activación de cuenta."""
    subject = "🦖 Verifica tu cuenta en DinoMascota Dashboard"
    purpose = "Activación de Cuenta de Usuario"

    if is_smtp_configured():
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = SMTP_FROM
            msg["To"] = to_email

            html_content = f"""
            <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #0f172a; color: #f8fafc; border-radius: 12px; padding: 32px; border: 1px solid #334155;">
                <div style="text-align: center; margin-bottom: 24px;">
                    <span style="font-size: 48px;">🦖</span>
                    <h1 style="color: #22c55e; margin: 8px 0;">DinoMascota Dashboard</h1>
                    <p style="color: #94a3b8; font-size: 14px;">Bases de Datos Aplicada — UAI</p>
                </div>
                <div style="background-color: #1e293b; border-radius: 8px; padding: 24px; text-align: center; border: 1px solid #475569;">
                    <h2 style="color: #ffffff; margin-top: 0;">¡Bienvenido, {username}!</h2>
                    <p style="color: #cbd5e1; font-size: 15px;">Para completar el registro y activar tu cuenta, ingresa el siguiente código de 6 dígitos:</p>
                    <div style="font-size: 32px; font-weight: bold; letter-spacing: 6px; color: #22c55e; background-color: #0f172a; padding: 14px 28px; border-radius: 8px; display: inline-block; margin: 16px 0; border: 1px dashed #22c55e;">
                        {code}
                    </div>
                    <p style="color: #94a3b8; font-size: 12px; margin-bottom: 0;">Este código vence en 15 minutos.</p>
                </div>
            </div>
            """
            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)

            return {"sent": True, "mode": "smtp", "message": "Correo enviado vía SMTP", "code": code}
        except Exception as e:
            print(f"[MAILER WARN] Falla al enviar por SMTP: {e}. Usando simulación local...")

    # Fallback / Modo Simulación Local
    print_simulated_email(to_email, username, subject, code, purpose)
    return {
        "sent": True, 
        "mode": "simulation", 
        "message": f"Código simulado para {to_email}: {code}", 
        "code": code
    }

def send_password_reset_email(to_email: str, username: str, code: str) -> Dict[str, Any]:
    """Envía o simula el correo con el código para recuperación de contraseña."""
    subject = "🔑 Restablecer contraseña - DinoMascota Dashboard"
    purpose = "Recuperación de Contraseña"

    if is_smtp_configured():
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = SMTP_FROM
            msg["To"] = to_email

            html_content = f"""
            <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #0f172a; color: #f8fafc; border-radius: 12px; padding: 32px; border: 1px solid #334155;">
                <div style="text-align: center; margin-bottom: 24px;">
                    <span style="font-size: 48px;">🦖</span>
                    <h1 style="color: #eab308; margin: 8px 0;">Recuperación de Contraseña</h1>
                    <p style="color: #94a3b8; font-size: 14px;">DinoMascota Dashboard — UAI</p>
                </div>
                <div style="background-color: #1e293b; border-radius: 8px; padding: 24px; text-align: center; border: 1px solid #475569;">
                    <h2 style="color: #ffffff; margin-top: 0;">Hola, {username}</h2>
                    <p style="color: #cbd5e1; font-size: 15px;">Recibimos una solicitud para restablecer tu contraseña. Tu código de seguridad temporal es:</p>
                    <div style="font-size: 32px; font-weight: bold; letter-spacing: 6px; color: #eab308; background-color: #0f172a; padding: 14px 28px; border-radius: 8px; display: inline-block; margin: 16px 0; border: 1px dashed #eab308;">
                        {code}
                    </div>
                    <p style="color: #94a3b8; font-size: 12px; margin-bottom: 0;">Si tú no realizaste esta solicitud, puedes ignorar este mensaje.</p>
                </div>
            </div>
            """
            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)

            return {"sent": True, "mode": "smtp", "message": "Correo enviado vía SMTP", "code": code}
        except Exception as e:
            print(f"[MAILER WARN] Falla al enviar por SMTP: {e}. Usando simulación local...")

    # Fallback / Modo Simulación Local
    print_simulated_email(to_email, username, subject, code, purpose)
    return {
        "sent": True, 
        "mode": "simulation", 
        "message": f"Código simulado para {to_email}: {code}", 
        "code": code
    }
