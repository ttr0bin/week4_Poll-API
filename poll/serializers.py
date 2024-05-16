from rest_framework import serializers

from poll.models import Poll

# 모든 속성
class PollSerializer(serializers.ModelSerializer):
    agreeRate = serializers.SerializerMethodField()
    disagreeRate = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ['id', 'title', 'description', 
                  'agree', 'disagree', 'agreeRate', 'disagreeRate',
                  'createdAt']
    
    def get_agreeRate(self, obj):
        total = obj.agree + obj.disagree
        if total == 0:
            return "No voting data yet"
        return obj.agree / total

    def get_disagreeRate(self, obj):
        total = obj.agree + obj.disagree
        if total == 0:
            return "No voting data yet"
        return obj.disagree / total