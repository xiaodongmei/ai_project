<template>
  <div class="upload-wrapper">
    <el-upload
      :action="action"
      :multiple="multiple"
      :file-list="fileList"
      :auto-upload="autoUpload"
      :accept="accept"
      :limit="limit"
      :on-change="handleChange"
      :on-exceed="handleExceed"
      :on-success="handleSuccess"
      :on-error="handleError"
      drag
      class="upload-area"
    >
      <el-icon class="el-icon--upload">
        <upload-filled />
      </el-icon>
      <div class="el-upload__text">
        拖拽文件到此或<em>点击上传</em>
      </div>
      <template #tip>
        <div class="el-upload__tip">
          {{ tipText }}
        </div>
      </template>
    </el-upload>

    <!-- 上传进度 -->
    <div v-if="showProgress && uploadProgress > 0" class="upload-progress">
      <el-progress :percentage="uploadProgress" />
    </div>

    <!-- 文件列表 -->
    <div v-if="fileList.length > 0" class="file-list">
      <div v-for="file in fileList" :key="file.uid" class="file-item">
        <span>{{ file.name }}</span>
        <el-icon class="remove-btn" @click="handleRemove(file)">
          <Close />
        </el-icon>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled, Close } from '@element-plus/icons-vue'

const props = defineProps({
  action: {
    type: String,
    required: true,
  },
  multiple: {
    type: Boolean,
    default: false,
  },
  autoUpload: {
    type: Boolean,
    default: true,
  },
  accept: {
    type: String,
    default: '*',
  },
  limit: {
    type: Number,
    default: 10,
  },
  maxSize: {
    type: Number,
    default: 10 * 1024 * 1024, // 10MB
  },
  showProgress: {
    type: Boolean,
    default: true,
  },
  tipText: {
    type: String,
    default: '支持拖拽或点击上传',
  },
})

const emit = defineEmits(['change', 'success', 'error', 'exceed'])

const fileList = ref([])
const uploadProgress = ref(0)

const handleChange = (file, files) => {
  // 检查文件大小
  if (file.size > props.maxSize) {
    ElMessage.error(`文件过大，请上传不超过 ${props.maxSize / 1024 / 1024}MB 的文件`)
    return
  }

  emit('change', { file, files })
}

const handleSuccess = (response, file, fileList) => {
  uploadProgress.value = 0
  ElMessage.success('上传成功')
  emit('success', { response, file, fileList })
}

const handleError = (error, file, fileList) => {
  uploadProgress.value = 0
  ElMessage.error('上传失败')
  emit('error', { error, file, fileList })
}

const handleExceed = (files, fileList) => {
  ElMessage.warning(`最多只能上传 ${props.limit} 个文件`)
  emit('exceed', { files, fileList })
}

const handleRemove = (file) => {
  const index = fileList.value.findIndex((f) => f.uid === file.uid)
  if (index > -1) {
    fileList.value.splice(index, 1)
  }
}
</script>

<style scoped lang="scss">
.upload-wrapper {
  .upload-area {
    :deep(.el-upload-dragger) {
      border: 2px dashed #dcdfe6;
      padding: 30px;

      &:hover {
        border-color: #409eff;
      }
    }
  }

  .upload-progress {
    margin-top: 15px;
  }

  .file-list {
    margin-top: 15px;

    .file-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px;
      background-color: #f5f7fa;
      border-radius: 4px;
      margin-bottom: 8px;

      span {
        flex: 1;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .remove-btn {
        cursor: pointer;
        color: #f56c6c;
        margin-left: 10px;

        &:hover {
          opacity: 0.8;
        }
      }
    }
  }
}
</style>
