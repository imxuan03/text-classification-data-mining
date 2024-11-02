from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pickle
import re
from pyvi import ViTokenizer


import re
from pyvi import ViTokenizer

class TextPreprocessor:
    def __init__(self, text, acronyms_file, stopwords_file):
        self.text = text
        self.stopwords = self.load_stopwords(stopwords_file)
        self.acronyms = self.load_acronyms(acronyms_file)

    def load_acronyms(self, filename):
        """Tải danh sách từ viết tắt từ file."""
        acronyms = []
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split(maxsplit=1)  # Tách bằng khoảng trắng đầu tiên
                    if len(parts) == 2:
                        acronyms.append((parts[0].strip(), parts[1].strip()))
        except FileNotFoundError:
            print(f"File {filename} không tồn tại.")
        return acronyms

    def load_stopwords(self, filename):
        """Tải danh sách từ dừng từ file."""
        stopwords = set()
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    stopwords.add(line.strip())
        except FileNotFoundError:
            print(f"File {filename} không tồn tại.")
        return stopwords
    
    def remove_punctuation(self, text):
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def segmentation(self):
        return ViTokenizer.tokenize(self.text)

    def split_words(self):
        text = self.segmentation()
        try:
            special_characters = '.,!?;:"\'()[]{}<>-'
            cleaned_words = [x.strip(special_characters).lower() for x in text.split()]
            return [self.remove_punctuation(word) for word in cleaned_words]
        except TypeError:
            return []

    def remove_loop_char(self):
        self.text = re.sub(r'([A-Z])\1+', lambda m: m.group(1).upper(), str(self.text), flags=re.IGNORECASE)
        self.text = re.sub(r'[^A-Za-zÀ-ỹ\s]', ' ', self.text)
        return self.text
        
    def replace_acronyms(self):
        """Thay thế các từ viết tắt."""
        list_text = self.text.split(" ")
        for i in range(len(list_text)):
            for acronym in self.acronyms:
                if list_text[i] == acronym[0]:
                    list_text[i] = acronym[1]
        self.text = " ".join(list_text)
        return self.text

    def remove_stopwords(self):
        split_words = self.split_words()
        words = []

        for word in split_words:
            if word not in self.stopwords:
                words.append(word)

        return ' '.join(words)

    def preprocess(self):
        self.text = self.remove_loop_char()
        self.text = self.replace_acronyms()
        self.text = self.remove_stopwords()
        return self.text



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pickle
import re
from pyvi import ViTokenizer

# Đường dẫn mô hình và vectorizer
model_paths = {
    "Naive Bayes": "E:/Khai Khoáng Dữ Liệu/Code/project/web/backend/backend/models/bayes_model.pkl",
    "KNN": "E:/Khai Khoáng Dữ Liệu/Code/project/web/backend/backend/models/knn_model.pkl",
    "SVM": "E:/Khai Khoáng Dữ Liệu/Code/project/web/backend/backend/models/svm_model.pkl",
}
vectorizer_path = "E:/Khai Khoáng Dữ Liệu/Code/project/web/backend/backend/models/tfidf_vectorizer.pkl"

# Danh mục các nhãn hoặc lớp dự đoán của mô hình văn bản
categories = ['Apps/Games', 'Internet', 'Mobile', 'Tin ICT', 'Xe']

# Tải TfidfVectorizer đã lưu
with open(vectorizer_path, 'rb') as f:
    vectorizer = pickle.load(f)

# Đường dẫn tới tệp từ viết tắt và từ dừng
acronyms_file = 'E:/Khai Khoáng Dữ Liệu/Code/project/acronym_vi.txt'
stopwords_file = 'E:/Khai Khoáng Dữ Liệu/Code/project/stopwords-nlp-vi.txt'

class TextDetectAPI(APIView):

    def post(self, request, *args, **kwargs):
        try:
            # Nhận dữ liệu JSON từ request
            data = request.data
            text_input = data.get('text')
            model_type = data.get('model')

            print(text_input)
            print(model_type)

            if not text_input:
                return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)

            # Tiền xử lý văn bản
            processed_text = self.prepare_text(text_input)

            # Chọn mô hình dựa trên loại mô hình
            if model_type not in model_paths:
                return Response({"error": "Model type not recognized"}, status=status.HTTP_400_BAD_REQUEST)

            model_path = model_paths[model_type]
            
            # Tải mô hình từ file .pkl
            with open(model_path, 'rb') as file:
                model = pickle.load(file)

            # Vector hóa văn bản đã tiền xử lý bằng TfidfVectorizer đã huấn luyện
            vectorized_text = vectorizer.transform([processed_text])

            # Dự đoán loại văn bản từ đầu vào
            predicted_class = model.predict(vectorized_text)
            label = categories[predicted_class[0]]

            # Trả về kết quả dự đoán
            return Response({'output': label})
        except Exception as e:
            print("Error:", str(e))  # In ra lỗi chi tiết để kiểm tra
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def prepare_text(self, text):
        # Sử dụng TextPreprocessor để tiền xử lý văn bản
        preprocessor = TextPreprocessor(text, acronyms_file, stopwords_file)
        return preprocessor.preprocess()
