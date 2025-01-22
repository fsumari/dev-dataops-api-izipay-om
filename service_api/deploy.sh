
export $(xargs < ../.env)

PROJECT_ID=$GCP_PROJECT_ID

DEPLOY_SERVICE_ACCOUNT=$DEPLOY_SERVICE_ACCOUNT
DEPLOY_SERVICE_NAME=$DEPLOY_SERVICE_NAME

REGION='us-central1'
CLOUD_RUN_PROJECT_NAME=$DEPLOY_SERVICE_NAME

echo $CLOUD_RUN_PROJECT_NAME
echo $REGION
echo $DEPLOY_SERVICE_ACCOUNT
echo 'project id-> ' $PROJECT_ID

gcloud run deploy ${CLOUD_RUN_PROJECT_NAME} \
    --region $REGION \
    --project $PROJECT_ID \
    --allow-unauthenticated \
    --cpu-boost \
    --cpu=1 \
    --memory=0.5G \
    --min-instances=0 \
    --max-instances=5 \
    --service-account $DEPLOY_SERVICE_ACCOUNT \
    --set-env-vars="GCP_PROJECT_ID=$PROJECT_ID" \
    --set-env-vars="SECRET_TOKEN=$SECRET_TOKEN" \
    --verbosity=debug \
    --source .

SERVICE_URL=$(gcloud run services describe $CLOUD_RUN_PROJECT_NAME --format 'value(status.url)' --project $PROJECT_ID --region $REGION)
echo "SERVICE_URL: $SERVICE_URL"
