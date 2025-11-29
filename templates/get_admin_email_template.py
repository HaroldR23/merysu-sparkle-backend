def get_admin_email_template(customer_name: str, customer_email: str, service_details: str, customer_message: str) -> str:
    return f"""
      <h2>New Quote Request Received</h2>
      <p><strong>Nombre del cliente:</strong> {customer_name}</p>
      <p><strong>Correo electrónico del cliente:</strong> {customer_email}</p>
      <p><strong>Detalles del servicio:</strong> {service_details}</p>
      <p><strong>Mensaje del cliente:</strong></p>
      <p>{customer_message}</p>
    """
