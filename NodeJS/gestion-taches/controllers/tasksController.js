// controllers/tasksController.js
const Task = require('../models/task');
const { createTaskSchema, updateTaskSchema } = require('../validators/taskValidator');
const fs = require('fs');
const path = require('path');

const tasksFile = path.join(__dirname, '../data/tasks.json');

// Charger les tâches depuis le fichier
function loadTasks() {
    if (fs.existsSync(tasksFile)) {
        const data = fs.readFileSync(tasksFile);
        return JSON.parse(data);
    }
    return [];
}

// Sauvegarder les tâches dans le fichier
function saveTasks(tasks) {
    fs.writeFileSync(tasksFile, JSON.stringify(tasks, null, 2));
}

let tasks = loadTasks();

// Obtenir toutes les tâches
exports.getTasks = (req, res) => {
    const { completed, search, page = 1, limit = 10 } = req.query;

    let filteredTasks = tasks;

    if (completed) {
        filteredTasks = filteredTasks.filter(task => String(task.completed) === completed);
    }

    if (search) {
        filteredTasks = filteredTasks.filter(task => task.title.toLowerCase().includes(search.toLowerCase()));
    }

    const startIndex = (page - 1) * limit;
    const endIndex = startIndex + parseInt(limit);
    const paginatedTasks = filteredTasks.slice(startIndex, endIndex);

    res.json(paginatedTasks);
};

// Ajouter une tâche
exports.createTask = (req, res) => {
    const { error } = createTaskSchema.validate(req.body);
    if (error) {
        return res.status(400).json({ error: error.details[0].message });
    }

    const { title } = req.body;
    const newTask = new Task(tasks.length + 1, title.trim(), false);
    tasks.push(newTask);
    saveTasks(tasks);
    res.status(201).json(newTask);
};

// Mettre à jour une tâche
exports.updateTask = (req, res) => {
    const { id } = req.params;
    const { error } = updateTaskSchema.validate(req.body);
    if (error) {
        return res.status(400).json({ error: error.details[0].message });
    }

    const task = tasks.find(t => t.id === parseInt(id));
    if (!task) return res.status(404).json({ error: 'Tâche non trouvée.' });

    const { title, completed } = req.body;
    if (title !== undefined) task.title = title.trim();
    if (completed !== undefined) task.completed = completed;

    saveTasks(tasks);
    res.json(task);
};

// Supprimer une tâche
exports.deleteTask = (req, res) => {
    const { id } = req.params;

    const index = tasks.findIndex(t => t.id === parseInt(id));
    if (index === -1) return res.status(404).json({ error: 'Tâche non trouvée.' });

    const deletedTask = tasks.splice(index, 1);
    saveTasks(tasks);
    res.json(deletedTask);
};
