<template>
    <div class="container">
        <div class="formInput">
            <div class="form-box">
                <form @submit.prevent="classifyText">
                    <label for="textInput" style="margin-right:5px;"><b>Enter text here for classification:</b></label>
                    <!-- <input v-model="textInput" class="input-text" type="text" id="textInput" placeholder="Type your text here" /> -->
                    <textarea v-model="textInput" class="input-text" id="textInput" placeholder="Type your text here"
                        rows="5"></textarea>

                    <label for="modelSelect" style="margin: 10px 0;"><b>Select Classification Model:</b></label>
                    <select v-model="selectedModel" class="dropdown" id="modelSelect">
                        <option disabled value="">Please select a model</option>
                        <option v-for="model in models" :key="model" :value="model">{{ model }}</option>
                    </select>

                    <button class="submit-button" type="submit"
                        :disabled="!textInput || !selectedModel">Classify</button>
                </form>
                <div v-if="loading">Loading...</div>
                <div v-else-if="error">{{ error }}</div>

                <div v-if="classificationResult" class="result-container">
                    <h4 style="margin:0; padding-right:5px;">Classification Result: </h4>
                    <p style="font-size:20px; margin:0;"><b> {{ classificationResult }}</b></p>
                </div>

            </div>
            <hr>
        </div>
    </div>
</template>

<script>
import PredictService from "../services/predict.service";

export default {
    data() {
        return {
            textInput: '',
            models: ['Naive Bayes', 'KNN', 'SVM'], // Replace with actual model names
            selectedModel: '',
            classificationResult: null,
            loading: false,
            error: null,
        };
    },
    methods: {
        async classifyText() {
            if (!this.textInput || !this.selectedModel) {
                this.error = 'Please enter text and select a model';
                return;
            }

            this.loading = true;
            this.error = null;
            this.classificationResult = null;

            try {
                const response = await PredictService.classifyText({
                    text: this.textInput,
                    model: this.selectedModel,
                });
                this.classificationResult = response.data.output; // Adjust based on API response
            } catch (error) {
                this.error = 'Failed to classify text';
                console.error(error);
            } finally {
                this.loading = false;
            }
        },
    }
};
</script>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
}

.form-box {
    border: 1px solid #ccc;
    padding: 30px;
    border-radius: 8px;
    margin-bottom: 16px;
    background-color: #f9f9f9;
    width: 100%;
}

.input-text {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    margin-bottom: 10px;
    height: 100px;
}

.dropdown {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    margin-bottom: 10px;
}

.submit-button {
    margin-top: 10px;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: bold;
}

.result-container {
    margin-top: 20px;
    text-align: center;
    display: flex; 
    align-items: center;
}
</style>
