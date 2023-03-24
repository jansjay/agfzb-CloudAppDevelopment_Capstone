const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {
    const authenticator = new IamAuthenticator({ apikey: "KEY" })
    console.log(1);
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    if(!params.selector){
        //any state "Texas, California etc.."
        params.selector = {"state": {"$regex": ".*"}};
    } else if(typeof params.selector === 'string'){
        //selector could be get (url encoded, e.g. selector=%7B"state"%3A%20"Texas"%7D or post {"selector": {"state": "Texas"}})
        params.selector = JSON.parse(params.selector);
    }
    console.log(2);
    cloudant.setServiceUrl("URL");
    console.log(3);
    return new Promise((resolve, reject) => {
        console.log(4);
        console.log(params.selector);
        cloudant.postFind({db:"dealerships",selector:params.selector})
            .then(response => {
                console.log(5);
                resolve(function(){ 
                    console.log(6);
                    console.log(params);
                    console.log(response.result.docs);
                    return {dealerships: response.result.docs}
                }());
                console.log(7);
            })
            .catch(err => {
                reject({ err: err });
            });
    });
}