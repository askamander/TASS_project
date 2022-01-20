import * as path from 'path';

import * as s3 from '@aws-cdk/aws-s3';
import * as cdk from '@aws-cdk/core';
import * as iam from '@aws-cdk/aws-iam';
import * as lambda from '@aws-cdk/aws-lambda';
import * as dynamodb from '@aws-cdk/aws-dynamodb';

export class ScrapersStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const bucket = new s3.Bucket(this, 'TASSDataStorage');

    const tassResultsTable = new dynamodb.Table(this, 'TASSResults', {
      partitionKey: { name: 'book_id', type: dynamodb.AttributeType.NUMBER },
      readCapacity: 1,
    });

    const readScaling = tassResultsTable.autoScaleWriteCapacity({
      minCapacity: 10,
      maxCapacity: 50,
    });

    readScaling.scaleOnUtilization({
      targetUtilizationPercent: 50,
    });

    const saveDataLambda = new lambda.Function(this, 'SaveData', {
      code: lambda.Code.fromAsset(path.join('lambda', 'save_data'), {
        bundling: {
          image: lambda.Runtime.PYTHON_3_8.bundlingImage,
          command: [
            'bash',
            '-c',
            'pip install -r requirements.txt -t /asset-output &&  rsync -av -O --progress . /asset-output --exclude-from=.dockerignore',
          ],
        },
      }),
      handler: 'index.handler',
      runtime: lambda.Runtime.PYTHON_3_8,
      timeout: cdk.Duration.minutes(1),
      environment: {
        LOG_LEVEL: '10',
        TABLE_NAME: tassResultsTable.tableName,
      },
    });

    tassResultsTable.grantWriteData(saveDataLambda);

    const queryWikidataLambda = new lambda.Function(this, 'QueryWikidata', {
      code: lambda.Code.fromAsset(path.join('lambda', 'query_wikidata'), {
        bundling: {
          image: lambda.Runtime.PYTHON_3_8.bundlingImage,
          command: [
            'bash',
            '-c',
            'pip install -r requirements.txt -t /asset-output &&  rsync -av -O --progress . /asset-output --exclude-from=.dockerignore',
          ],
        },
      }),
      handler: 'index.handler',
      runtime: lambda.Runtime.PYTHON_3_8,
      timeout: cdk.Duration.minutes(1),
      environment: {
        LOG_LEVEL: '10',
        WIKIDATA_API_URL: 'https://query.wikidata.org/sparql',
        SAVE_DATA_LAMBDA: saveDataLambda.functionName,
      },
    });

    queryWikidataLambda.addToRolePolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ['lambda:InvokeFunction'],
        resources: [saveDataLambda.functionArn],
      })
    );

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
      handler: 'index.handler',
      runtime: lambda.Runtime.PYTHON_3_8,
      timeout: cdk.Duration.minutes(1),
      environment: {
        LOG_LEVEL: '10',
        QUERY_WIKIDATA_LAMBDA: queryWikidataLambda.functionName,
      },
    });

    wikidataScraperLambda.addToRolePolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ['lambda:InvokeFunction'],
        resources: [queryWikidataLambda.functionArn],
      })
    );

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
        handler: 'index.handler',
        runtime: lambda.Runtime.PYTHON_3_8,
        timeout: cdk.Duration.minutes(15),
        environment: {
          LOG_LEVEL: '10',
          SCRAPER_LAMBDA: wikidataScraperLambda.functionName,
          DATASET_PATH: 'unique_authors_wiki_1.csv',
        },
      }
    );

    wikidataScraperOrchestratorLambda.addToRolePolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW,
        actions: ['lambda:InvokeFunction'],
        resources: [wikidataScraperLambda.functionArn],
      })
    );
  }
}
