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

## 2. Upload Image to Container Registry
    ```sh
    cd $DIRECTORY_BASE
    cp ../.env .env
    export $(xargs < ../.env)
    gcloud builds submit --tag=gcr.io/$PROJECT_ID/$IMAGE_NAME --project $PROJECT_ID --suppress-logs .
    ```

## 3. Deploy

    ```sh
     cd chatbot-container
     bash deploy.sh
    ```
