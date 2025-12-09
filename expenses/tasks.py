from celery import shared_task
import time

@shared_task
def heavy_process_simulation(duration):
    """
    Bu fonksiyon sanki çok ağır bir rapor hazırlıyormuş gibi sistemi verilen süre kadar uyutacak(meşgul edecek).
    """

    print(f"Heavy process {duration} saniyeliğine başladı.")
    time.sleep(duration)
    print("Heavy process tamamlandı.")
    return f"{duration} saniyelik işlem tamamlandı"