import dns.resolver

from domain.src.ports.EmailVerifierService import EmailVerifierService


"""This serive will have to be replaced with a third-party email verification service in the future"""
class EmailVerifierAdapter(EmailVerifierService):
    async def verify_email(self, email: str) -> bool:
        domain = email.split("@")[-1]
        try:
            answers = dns.resolver.resolve(domain, "MX")
            for rdata in answers:
                exchange = str(rdata.exchange).rstrip(".")
                if exchange == "":  # MX pointing to root
                    return False
            return True
        except:
            return False
