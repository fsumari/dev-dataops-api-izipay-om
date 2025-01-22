# dev-dataops-api-izipay-om
APIs de DataOps para diferentes casos de uso.

# Izipay - API Hashing

## 1. Clone repository

* Clone tradicional

    ```sh
     git clone https://github.com/fsumari/dev-dataops-api-izipay-om.git
    ```

* Or clone with Personal Token
  
    ```sh
    GITHUB_REPOSITORY=github.com/fsumari/dev-dataops-api-izipay-om.git
    GITHUB_TOKEN=xxxxxxxxxxxxxxx
    GITHUB_USERNAME=xxxxxxxxxxxxx
    git clone https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@${GITHUB_REPOSITORY}
    ```

## 2. Crear Service Account

Crear SA con el siguiente comando:

```
gcloud iam service-accounts create prd-dataops-apis-onemarketer \
  --display-name "Service account para dataops apis"
```

## 3. Dar permisos a la Service Account

Obtener el ID del projecto.

```
export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value core/project)
```
Permisos de User para las APIS , DocAI y Firestore:

```

gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
    --member="serviceAccount:prd-dataops-apis-onemarketer@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
    --role="roles/datastore.user"

gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
    --member="serviceAccount:prd-dataops-apis-onemarketer@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
    --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
    --member="serviceAccount:prd-dataops-apis-onemarketer@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
    --role="roles/viewer"
```


## 4. Deploy

    ```sh
     cd service_api
     bash deploy.sh
    ```
