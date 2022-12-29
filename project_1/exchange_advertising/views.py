
import pika
import boto3
import logging
import requests

from .models import *
from queue import Empty
from turtle import clear
from urllib import request
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from botocore.exceptions import ClientError
from rest_framework.response import Response
from .serializers import advertisingSerializer
from django.shortcuts import get_object_or_404
from .thread import Thread
# Create your views here.

class setAdvertisingView(APIView):
    def post(self, request):
        saved_data = {
            'description': request.data['description'],
            'email': request.data['email']
        }  
        ser = advertisingSerializer(data=saved_data)
        id = 0
        if ser.is_valid():
            ser.save()
            id = ser.data['id']
            logging.basicConfig(level=logging.INFO)
            try:
                s3_resource = boto3.resource(
                    's3',
                    endpoint_url='https://s3.ir-thr-at1.arvanstorage.com',
                    aws_access_key_id='02b30e30-6a9f-4103-a1ef-454394ecc666',
                    aws_secret_access_key='a7844e6ae459c81f4852394463bc4cf35cb43700'
                )
            except Exception as exc:
                logging.error(exc)
            else:
                try:
                    bucket = s3_resource.Bucket('cloudhw')
                    bucket.put_object(
                        ACL='public-read',
                        Body=request.data['image'],
                        Key=str(id)+'.jpg'
                    )
                except ClientError as e:
                    logging.error(e)
            ad = get_object_or_404(advertising, id=id)
            ad.image = 'https://cloudhw.s3.ir-thr-at1.arvanstorage.com/' + str(id)+'.jpg'
            ad.save()
            
            Thread.delay(id,request.data['email'])
            return Response(f'Your ad is succesfully aded and  in the review queue your id is {str(id)}',status=status.HTTP_202_ACCEPTED)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        id = request.query_params.get('id', None)
        ad = get_object_or_404(advertising, id=id)
        ser = advertisingSerializer(ad)
        if ser.data['state'] == 1:
            copy=ser.data
            copy['state']="confirmed"
            return Response(copy,status=status.HTTP_202_ACCEPTED)
        elif ser.data['state'] == 2:
                return Response('Your ad is in the review queue',status=status.HTTP_204_NO_CONTENT)
        elif ser.data['state'] == 3:
                return Response('Your ad is not confirmed',status=status.HTTP_406_NOT_ACCEPTABLE)     
        return Response('invalid id', status=status.HTTP_400_BAD_REQUEST)

