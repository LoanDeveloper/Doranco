// validators/taskValidator.js
const Joi = require('joi');

const createTaskSchema = Joi.object({
    title: Joi.string().required().messages({
        'string.base': `"title" doit être une chaîne de caractères`,
        'string.empty': `"title" ne peut pas être vide`,
        'any.required': `"title" est requis`
    })
});

const updateTaskSchema = Joi.object({
    title: Joi.string().optional(),
    completed: Joi.boolean().optional()
});

module.exports = {
    createTaskSchema,
    updateTaskSchema
};
