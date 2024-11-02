from django.db import models

class Text_Prediction(models.Model):
    text_input = models.TextField()  # Trường này lưu trữ văn bản nhập vào
    model_type = models.CharField(max_length=50)  # Trường này lưu tên mô hình được chọn
    prediction = models.CharField(max_length=50, blank=True, null=True)  # Lưu trữ kết quả phân loại

    def __str__(self):
        return f"{self.model_type} prediction for text: {self.text_input[:30]}..."