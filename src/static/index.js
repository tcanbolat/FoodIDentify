const { createApp } = Vue

const app = createApp({
  data() {
    return {
      uploadedImageFile: null,
      previewImgUrl: '',
      PredictedResult: '',
      loading: false
    }
  },
  methods: {
    onClickUploadIcon() {
      this.$refs.uploadInput.click()
    },
    handleImageUpload(event) {
      const file = event.target.files[0]
      this.uploadedImageFile = file

      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        this.previewImgUrl = reader.result;
      }
    },
    predictImage() {
      this.loading = true

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
        console.log(err)
      })
    },
    reset () {
      this.uploadedImageFile = null
      this.previewImgUrl = ''
      this.PredictedResult = ''
      this.loading = false
    }
  },
})

app.config.compilerOptions.delimiters = ["${","}"]
app.mount('#wrapper')
