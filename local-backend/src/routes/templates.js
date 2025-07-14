const express = require('express');
const router = express.Router();
const templatesController = require('../controllers/templatesController');
const multer = require('multer');
const path = require('path');

const upload = multer({ dest: path.join(__dirname, '../../templates') });

// 获取所有模板元数据
router.get('/', templatesController.getAllTemplates);
// 上传新模板
router.post('/', upload.single('file'), templatesController.uploadTemplate);
// 获取单个模板内容
router.get('/:id', templatesController.getTemplateById);
// 删除模板
router.delete('/:id', templatesController.deleteTemplate);

module.exports = router;