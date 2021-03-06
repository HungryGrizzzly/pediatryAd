<template>
  <div class="create_ad_container">
    <preloader v-if="isLoading" />
    <div v-else class="create_ad_wrapper">
      <form class="create_form">
        <div class="left_block">
          <input
            type="file"
            name="fileUpload"
            id="file_upload"
            ref="file_upload"
            @change="changeHandler"
          />
          <div class="drop_zone" :class="{'error': error.image}">
            <img
              id="create_img"
              v-if="this.photo.url"
              :src="this.photo.url"
              alt="Так изображение будет выглядеть в приложении"
            />
            <svg
              v-else
              width="39"
              height="39"
              viewBox="0 0 39 39"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M29.8185 34.4594H4.42735V9.06825H20.7502V5.44095H4.42735C2.43233 5.44095 0.800049 7.07324 0.800049 9.06825V34.4594C0.800049 36.4544 2.43233 38.0867 4.42735 38.0867H29.8185C31.8135 38.0867 33.4458 36.4544 33.4458 34.4594V18.1365H29.8185V34.4594ZM15.6901 28.7101L12.1354 24.4299L7.14783 30.8321H27.098L20.6777 22.2898L15.6901 28.7101ZM33.4458 5.44095V0H29.8185V5.44095H24.3775C24.3956 5.45909 24.3775 9.06825 24.3775 9.06825H29.8185V14.4911C29.8366 14.5092 33.4458 14.4911 33.4458 14.4911V9.06825H38.8867V5.44095H33.4458Z"
                fill="#DCDCDC"
              />
            </svg>
          </div>
          <div class="upload_btn" @click="uploadBtnClickHandler">Загрузить</div>
        </div>
        <div class="right_block">
          <input
            name="title"
            id="title"
            :class="{'error': error.title}"
            type="text"
            placeholder="Заголовок..."
            @input="inputHandler"
          />
          <textarea
            name="description"
            id="description"
            :class="{'error': error.description}"
            cols="50"
            rows="5"
            placeholder="Рекламный текст..."
            @input="inputHandler"
          ></textarea>
          <div class="create_fields_wrapper">
            <input
              type="url"
              name="product_url"
              id="product_url"
              :class="{'error': error.product_url}"
              placeholder="Ссылка на ресурс рекламодателя"
              @input="inputHandler"
            />
            <select-base :setIndex="setIndex" :error="error.index" />
          </div>
          <div class="create_fields_wrapper">
            <input
              type="url"
              name="video_url"
              id="video_url"
              :class="{'error': error.video_url}"
              placeholder="Добавить видео (URL)"
              @input="inputHandler"
            />
            <input-date :updating="false" :error="error.time" :set_value="setTimes" />
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import toastr from "toastr";
import { isNull } from "util";
import InputDate from "../../components/input/date/InputDate";
import {
  stringToTimestamp,
  clearNumbers,
  validURL
} from "../../utils/common.utils";
import SelectBase from "../../components/selectors/SelectorBase";
import Preloader from "../../components/preloader/Preloader";

export default {
  name: "create_ad_form",
  data: () => ({
    title: "",
    description: "",
    product_url: "",
    video_url: "",
    index: "",
    photo: {
      file: null,
      url: null
    },
    time: {
      text: '',
      start_time: null,
      end_time: null
    },
    error: {
      title: false,
      description: false,
      product_url: false,
      video_url: false,
      index: false,
      image: false,
      time: false
    }
  }),
  components: {
    "input-date": InputDate,
    "select-base": SelectBase,
    preloader: Preloader
  },
  computed: {
    timeIsEmpty() {
      return isNull(this.time.start_time);
    },
    isLoading() {
      return this.$store.getters.LOADING;
    }
  },
  methods: {
    uploadBtnClickHandler: uploadBtnClickHandler,
    inputHandler: inputHandler,
    changeHandler: changeHandler,
    createAd: createAd,
    setTimes: setTimes,
    setIndex: setIndex
  },
};

function setIndex(index) {
  this.error.index = false;
  this.index = index;
}

function uploadBtnClickHandler() {
  this.$refs.file_upload.click();
}

function inputHandler({ target }) {
  const { id, value } = target;
  if (value.length == 0) {
    this.error[id] = true;
  } else {
    this.error[id] = false;
  }
  this.$data[id] = value;
}

function changeHandler() {
  const file_upload = this.$refs.file_upload;
  if (file_upload.files && file_upload.files[0]) {
    const reader = new FileReader();
    const file = file_upload.files[0];
    reader.onload = ({ target }) => {
      const allowedTypes = ["image/jpg", "image/jpeg", "image/png"];
      const { result } = target;
      for (let type of allowedTypes) {
        if (file.type === type) {
          this.photo = {
            file: file,
            url: result
          };
        }
      }
      if (this.photo.url !== result) {
        toastr.error(
          "Данный тип файлов не поддерживется. Разрешенные форматы изображений: jpg, jpeg и png"
        );
      }
    };
    reader.readAsDataURL(file_upload.files[0]);
    this.error.image = false;
  }
}

function createAd() {
  this.error = validateData(this.$data);
  for (let key in this.error) {
    if (this.error[key]) {
      toastr.error("Все необходимые поля должны быть заполнены");
      return;
    }
  }
  
  let formData = new FormData();

  formData.append("token", JSON.parse(localStorage.getItem("TOKEN")));
  formData.append("title", this.title);
  formData.append("description", this.description);
  formData.append("video_url", this.video_url);
  formData.append("product_url", this.product_url);
  formData.append("image", this.photo.file);
  formData.append("start_time", this.time.start_time);
  formData.append("end_time", this.time.end_time);
  formData.append("index", this.index);
  formData.append("active", true);
  formData.append("show_image", true);
  this.$store.dispatch("create_ad", formData);
}

function validateData(data) {
  let error = {
    title: false,
    description: false,
    product_url: false,
    video_url: false,
    index: false,
    image: false,
    time: false
  };
  if (data.title.length == 0) {
    error.title = true;
  }
  if (data.description.length == 0) {
    error.description = true;
  }
  if (data.product_url.length == 0) {
    error.product_url = true;
  }
  if (data.video_url.length > 0 && !validURL(data.video_url)) {
    error.video_url = true;
    toastr.error("Ссылка на видео введена некорректно");
  }
  if (data.product_url.length > 0 && !validURL(data.product_url)) {
    error.product_url = true;
    toastr.error("Ссылка на ресурс рекламодателя введена некорректно");
  }
  if (data.index.length == 0) {
    error.index = true;
  }
  if (!data.photo.file) {
    error.image = true;
  }

  if (data.time.text.length > 0 && clearNumbers(data.time.text).length < 16) {
    toastr.error("Период активности кампании введен некорректно");
    error.time = true;
  }

  if (data.time.text && clearNumbers(data.time.text).length == 16) {
    if (data.time.start_time >= data.time.end_time) {
      toastr.error("Дата начала не может быть больше или равна дате окончания");
      error.time = true;
    }
  }
  return error;
}

function setTimes(time) {
  this.error.time = time.length == 0;

  const { start_time, end_time } = stringToTimestamp(time);
  this.time = {
    text: clearNumbers(time),
    start_time: start_time ? start_time : null,
    end_time: end_time ? end_time : null
  };
}
</script>

<style lang="scss" src="./style.scss" scoped>
</style>