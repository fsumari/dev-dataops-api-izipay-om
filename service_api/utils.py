from google.cloud import firestore
import hashlib
from datetime import datetime, date
from typing import Optional, Dict, List
import uuid

class FirestoreLogs:
    def __init__(self, project_id:str, database_id:str, collection_name: str = "logs"):
        """
        Inicializa la conexión con Firestore.
        
        Args:
            collection_name (str): Nombre de la colección en Firestore
        """
        self.db = firestore.Client(project=project_id, database=database_id)
        self.collection = self.db.collection(collection_name)
    
    def _hash_ruc(self, ruc: str) -> str:
        """
        Procesa el RUC para determinar el código del tipo de RUC (COD_TIP_RUC)
        y calcula el hash final (INTER_HASH_URC).

        Parámetros:
            ruc (str): Número de RUC.

        Retorna:
            dict: Un diccionario con el RUC original, COD_TIP_RUC e INTER_HASH_URC.
        """
        # Convertir a cadena y eliminar espacios
        ruc = str(ruc).strip()

        # Determinar el código del tipo de RUC (COD_TIP_RUC)
        if len(ruc) == 8:
            cod_tip_ruc = '01'
        elif len(ruc) == 9 or (10 <= len(ruc) <= 12 and ruc[0] == '0'):
            cod_tip_ruc = '02'
        elif len(ruc) == 11 and ruc[:2] in ['20', '17', '15', '10', '12', '11']:
            cod_tip_ruc = '03'
        else:
            cod_tip_ruc = '06'

        # Rellenar el RUC con ceros a la izquierda hasta 15 caracteres
        padded_ruc = cod_tip_ruc + ruc.zfill(15)

        # Calcular el hash SHA256 anidado
        inner_hash = hashlib.sha256(padded_ruc.encode()).hexdigest().upper()
        inter_hash_urc = hashlib.sha256(inner_hash.encode()).hexdigest().upper()

        # Retornar los resultados
        # Calcular y retornar el hash SHA256
        return inter_hash_urc

    def store_log(self, ruc: str) -> Dict[str, str]:
        """
        Almacena un nuevo log en Firestore usando un ID único.
        
        Args:
            ruc (str): RUC a almacenar
            
        Returns:
            Dict[str, str]: Datos almacenados incluyendo el hash generado
        """
        
        ruc_hash = self._hash_ruc(ruc)
        
        log_data = {
            'timestamp_consulta': datetime.now(),
            'ruc': ruc,
            'ruc_hasheado': ruc_hash,
            'process_date': date.today().strftime("%d-%m-%Y"),
            'record_source': 'API_IZIPAY',
            'load_date': datetime.now(),
            'creation_user': 'ETL_USER'
        }
        
        # Generar ID único para cada log
        doc_id = str(uuid.uuid4())
        self.collection.document(doc_id).set(log_data)
        
        return ruc_hash, log_data
    
    def get_ruc_by_hash(self, ruc_hash: str) -> List[Dict]:
        """
        Busca todos los registros asociados a un hash de RUC.
        
        Args:
            ruc_hash (str): Hash del RUC a buscar
            
        Returns:
            List[Dict]: Lista de todos los registros encontrados, ordenados por fecha
        """
        docs = (self.collection
                .where('ruc_hasheado', '==', ruc_hash)
                .order_by('fecha_process', direction=firestore.Query.DESCENDING)
                .stream())
        
        return [doc.to_dict() for doc in docs]
    
    def get_latest_ruc_by_hash(self, ruc_hash: str) -> Optional[str]:
        """
        Obtiene el RUC más reciente asociado a un hash.
        
        Args:
            ruc_hash (str): Hash del RUC a buscar
            
        Returns:
            Optional[str]: RUC más reciente si se encuentra, None si no existe
        """
        docs = (self.collection
                .where('ruc_hasheado', '==', ruc_hash)
                .order_by('load_date', direction=firestore.Query.DESCENDING)
                .limit(1)
                .stream())
        
        for doc in docs:  # Solo tomará el primer documento
            return doc.to_dict().get('ruc')
        return None

    def get_ruc_history(self, ruc: str) -> List[Dict]:
        """
        Obtiene todo el historial de logs para un RUC específico.
        
        Args:
            ruc (str): RUC del cual obtener el historial
            
        Returns:
            List[Dict]: Lista de todos los logs asociados al RUC
        """
        ruc_hash = self._hash_ruc(ruc)
        return self.get_ruc_by_hash(ruc_hash)
