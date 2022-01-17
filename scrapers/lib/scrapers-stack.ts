import * as path from 'path';

import * as s3 from '@aws-cdk/aws-s3';
import * as cdk from '@aws-cdk/core';
import * as iam from '@aws-cdk/aws-iam';
import * as lambda from '@aws-cdk/aws-lambda';

export class ScrapersStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const bucket = new s3.Bucket(this, 'TASSDataStorage');

    const wikidataScraperLambda = new lambda.Function(this, 'WikidataScraper', {
      code: lambda.Code.fromAsset(path.join('lambda', 'wikipedia_scraper'), {
        bundling: {
          image: lambda.Runtime.PYTHON_3_8.bundlingImage,
          command: [
            'bash',
            '-c',
            'pip install -r requirements.txt -t /asset-output &&  rsync -av -O --progress . /asset-output --exclude-from=.dockerignore',
          ],
        },
      }),
      handler: 'index.handler', // Optional, defaults to 'handler'
      runtime: lambda.Runtime.PYTHON_3_8, // Optional, defaults to lambda.Runtime.PYTHON_3_7
      timeout: cdk.Duration.minutes(1),
      environment: {
        LOG_LEVEL: '10', // Debug log level - https://docs.python.org/3/library/logging.html
      },
    });

    const wikidataScraperOrchestratorLambda = new lambda.Function(
      this,
      'WikidataScraperOrchestrator',
      {
        code: lambda.Code.fromAsset(
          path.join('lambda', 'wikipedia_scraper_orchestrator'),
          {
            bundling: {
              image: lambda.Runtime.PYTHON_3_8.bundlingImage,
              command: [
                'bash',
                '-c',
                'pip install -r requirements.txt -t /asset-output &&  rsync -av -O --progress . /asset-output --exclude-from=.dockerignore',
              ],
            },
          }
        ),
        handler: 'index.handler', // Optional, defaults to 'handler'
        runtime: lambda.Runtime.PYTHON_3_8, // Optional, defaults to lambda.Runtime.PYTHON_3_7
        timeout: cdk.Duration.minutes(15),
        environment: {
          LOG_LEVEL: '10', // Debug log level - https://docs.python.org/3/library/logging.html
          SCRAPER_LAMBDA: wikidataScraperLambda.functionName,
        },
      }
    );

    wikidataScraperOrchestratorLambda.addToRolePolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: [
          'lambda:InvokeFunction',
        ],
        resources: [wikidataScraperLambda.functionArn],
      }),
    );
  }
}
