import requests
import os

class ExpenseAnalytics:
    def __init__(self, user):
        self.user = user

    def analyze_receipt_via_fastapi(self, image_file):
        """
        Gelen dosya objesini FastAPI servisine iletir.
        """
        # Ortam değişkeninden URL al, yoksa varsayılan Docker adresini kullan
        base_url = os.environ.get('AI_SERVICE_URL', 'http://ai_service:8001')
        fastapi_url = f"{base_url}/analyze/"
        
        try:
            # Dosyayı FastAPI'ye gönderme işlemi(Multipart Upload)
            # image_file.name dosya adını, image_file ise binary içeriği verir
            files = {'file': (image_file.name, image_file, image_file.content_type)}
            
            # files parametresi ile gönderince requests otomatik header ayarlar
            response = requests.post(fastapi_url, files=files, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"AI Servis Hatasi ({response.status_code}): {response.text}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Baglanti Hatasi: {str(e)}"}