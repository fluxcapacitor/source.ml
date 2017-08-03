# ingress.ml

Create simple ingress rules using the [ingress-nginx](https://github.com/kubernetes/kops/tree/master/addons/ingress-nginx) 
[KOPS/addons](https://github.com/kubernetes/kops/tree/master/addons) that work with route53 hosted zone cname records to 
route inbound connections to cluster services.

* [v1.6.0-gce.yaml](https://github.com/kubernetes/kops/blob/master/addons/ingress-nginx/v1.6.0-gce.yaml)
* [v1.6.0.yaml](https://github.com/kubernetes/kops/blob/master/addons/ingress-nginx/v1.6.0.yaml)

The configurations implemented in this ingress-nginx application use a wildcard ssl cert that must be generated separately for
SSL/TLS authentication.

#### ingress - certs

Execute `sudo bash generate-wildcard-ssl-cert.sh` to generate an rsa key and wildcard certificate required to use SSL with the 
ingress-nginx internal load balancer service.

```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt \
 -subj "/C=US/ST=California/L=San Francisco/O=Pipeline.IO/CN=*.pipeline.io/emailAddress=chris@fregly.com"
sudo openssl x509 -noout -fingerprint -text < tls.crt > tls-wildcard.info
sudo cat tls.crt tls.key > tls.pem
```

Create a `tls-certificate` secret in each namespace containing ingress rules. 
```
kubectl create secret tls tls-certificate --key tls.key --cert tls.crt
```

#### AWS

Use the following AWS Certificate Manager API command to import the wildcard certificate
```
aws acm import-certificate --certificate file://tls.pem --private-key file://tls.pem
```

When the preceding command is successful, it returns the [Amazon Resource Name (ARN)](http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html)
 of the imported certificate.  You can also use the following AWS cli command to identify the ARN for your ssl cert:  
```
aws acm list-certificates
```

For more information about how to import your wildcard certificate into AWS Certificate Manager see [Importing Certificates 
into AWS Certificate Manager](http://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html) 

### ingress-nginx deploy

Kubernetes uses the [service.beta.kubernetes.io/aws-load-balancer-ssl-cert](https://github.com/kubernetes/kubernetes/blob/master/pkg/cloudprovider/providers/aws/aws.go#L121) 
annotation on services to request a secure listener.  Update the service.beta.kubernetes.io/aws-load-balancer-ssl-cert 
annotation in ingress-nginx-v1.6.0-app.yaml replacing the following text with the arn returned by the AWS cli command above: 
```
arn:aws:acm:<aws-region>:<account>:certificate/<uuid>
```

Deploy ingress-nginx
```
kubectl apply -f ingress-nginx-v1.6.0-app.yaml
```

##### Create Route53 CNAME's

Use the following AWS CLI command to get the hosted-zone-id for the `pipeline.io.` Route53 Hosted Zone.
```
hosted_zone_id=$(
  aws route53 list-hosted-zones \
    --output text \
    --query 'HostedZones[?Name==`'pipeline.io'.`].Id'
)
echo hosted_zone_id=$hosted_zone_id
```

Use the following AWS CLI command to get the dnsname of the internal elb that was created by the ingress-nginx deploy above.  
```
internal_elb_dnsname=$(
  aws elb describe-load-balancers | jq -r '[.LoadBalancerDescriptions[]
  | select(.BackendServerDescriptions[].PolicyNames[] == "k8s-proxyprotocol-enabled")][0]| .DNSName '
)
echo internal_elb_dnsname=$internal_elb_dnsname
```

Execute the following AWS CLI command to create a prediction-python3.pipeline.io. CNAME record set in the `pipeline.io.` 
Route53 Hosted Zone.
```
aws route53 change-resource-record-sets --hosted-zone-id $hosted_zone_id \
--change-batch '{
                  "Comment": "prediction-python3 cname record set for the zone.",
                  "Changes": [
                    {
                      "Action": "CREATE",
                      "ResourceRecordSet": {
                        "Name": "prediction-python.pipeline.io.",
                        "Type": "CNAME",
                        "TTL": 60,
                        "ResourceRecords": [
                          {
                            "Value": '"$internal_elb_dnsname"'
                          }
                        ]
                      }
                    }
                  ]
                }'
```

