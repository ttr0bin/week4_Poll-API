from django.shortcuts import render
from rest_framework import status
from poll.models import Poll
from poll.serializers import PollSerializer, PollRequestSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response


# poll list 전체 출력하거나 새로운 poll 생성
@api_view(['GET', 'POST'])
def poll_list(request):
    match request.method:
        case 'GET':
            match request.query_params.get("order", "latest"):
                case 'latest'   : poll = Poll.objects.all().order_by('-createdAt')
                case 'oldest'   : poll = Poll.objects.all().order_by('createdAt')
                case 'agree'    : poll = Poll.objects.all().order_by('-agree')
                case 'disagree' : poll = Poll.objects.all().order_by('-disagree')

            serializer = PollSerializer(poll, many=True)
            return Response(serializer.data)
        case 'POST':
            serializer = PollRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 각 poll에 대한 조치 (보기, 수정, 삭제)
@api_view(['GET', 'PUT', 'DELETE'])
def poll_detail(request, id):
    try:
        poll = Poll.objects.get(id=id)
    except Poll.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    match request.method:
        case 'GET':
            serializer = PollSerializer(poll)
            return Response(serializer.data)
        case 'PUT':
            serializer = PollRequestSerializer(poll, data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        case 'DELETE':
            poll.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


# poll_agree와 disagree
@api_view(['POST'])
def poll_agree(request, id):
    try:
        poll = Poll.objects.get(id=id)
    except Poll.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    poll.agree += 1
    poll.save()
    serializer = PollSerializer(poll)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def poll_disagree(request, id):
    try:
        poll = Poll.objects.get(id=id)
    except Poll.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    poll.disagree += 1
    poll.save()
    serializer = PollSerializer(poll)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)