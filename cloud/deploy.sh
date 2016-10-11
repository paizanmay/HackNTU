ecs-cli configure --region ap-northeast-1 --access-key AKIAJLROQZ4DSXSQKKVA --secret-key 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 --cluster hackntu
ecs-cli compose -f docker-compose-deploy.yml service stop && \
ecs-cli compose -f docker-compose-deploy.yml service up
