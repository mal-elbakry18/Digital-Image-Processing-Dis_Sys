

 
        // AWS Configuration
        AWS.config.region = 'your-region'; // Replace 'your-region' with your AWS region
        AWS.config.credentials = new AWS.CognitoIdentityCredentials({
            IdentityPoolId: 'us-east-1_ObGK69kA3' // Replace 'your-identity-pool-id' with your Cognito Identity Pool ID
        });

        // Cognito User Pool Configuration
        var poolData = {
            UserPoolId: 'your-user-pool-id', // Replace 'your-user-pool-id' with your Cognito User Pool ID
            ClientId: 'your-client-id' // Replace 'your-client-id' with your Cognito Client ID
        };
        var userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

