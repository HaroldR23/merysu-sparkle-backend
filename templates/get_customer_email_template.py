def get_customer_email_template(customer_name: str) -> str:
    return f"""
      <h2>Thank You for Your Quote Request, {customer_name}!</h2>
      <p>We have received your request and will get back to you shortly.</p>
      <p>Best regards,<br/>The Merysu Sparkle Team</p>
    """
