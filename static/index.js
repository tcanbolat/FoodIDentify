const { createApp } = Vue

const app = createApp({
  data() {
    return {
      uploadedImageFile: null,
      previewImgUrl: '',
      PredictedResult: {},
      loading: false,
      error: false,
      step: {
        welcome: true,
        chooseFood: false,
        uploadFood: false,
        predictFood: false
      }
    }
  },
  methods: {
    updateStep(prevStep, nextStep) {
      this.step[prevStep] = false
      this.step[nextStep] = true
    },
    onClickUploadIcon() {
      this.$refs.uploadInput.click()
    },
    handleImageUpload(event) {
      const file = event.target.files[0]
      this.uploadedImageFile = file

      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => {
        this.previewImgUrl = reader.result
      }
      this.step.uploadFood = false
      this.step.predictFood = true
    },
    predictImage() {
      this.loading = true
      this.error = false

      const data = new FormData()
      data.append('file', this.uploadedImageFile)
      const config = {
        header : {
         'Content-Type' : 'multipart/form-data'
       }
      }

      const self = this

      axios.post(window.location.href + '/predict', data, config)
      .then(res => {
        self.loading = false
        self.PredictedResult = res.data.prediction
      })
      .catch(err => {
        self.loading = false
        self.error = true
        console.log(err)
      })
    },
    reset () {
      this.uploadedImageFile = null
      this.previewImgUrl = ''
      this.PredictedResult = ''
      this.loading = false
      this.step.predictFood = false
      this.step.welcome = true
    }
  },
})

app.config.compilerOptions.delimiters = ["${","}"]
app.mount('#wrapper')
