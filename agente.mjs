    import ollama from 'ollama';
import chalk from 'chalk';
import ora from 'ora';
import fs from 'fs/promises';
import inquirer from 'inquirer';

const MODELO = 'qwen3-coder'; // Asegúrate que es el nombre en tu 'ollama list'

async function procesarConIA(instruccion, contenidoActual = '') {
    const spinner = ora('El modelo está procesando...').start();
    try {
        const response = await ollama.chat({
            model: MODELO,
            messages: [
                { 
                    role: 'system', 
                    content: 'Eres un asistente de programación CLI. Si se te pide modificar, devuelve SOLO el nuevo contenido del archivo, sin explicaciones ni bloques de código markdown.' 
                },
                { 
                    role: 'user', 
                    content: `Archivo actual:\n${contenidoActual}\n\nInstrucción: ${instruccion}` 
                },
            ],
        });
        spinner.stop();
        return response.message.content.trim();
    } catch (error) {
        spinner.stop();
        console.error(chalk.red('Error en Ollama:'), error.message);
        return null;
    }
}

async function menuPrincipal() {
    console.log(chalk.magenta.bold('\n--- PANEL DE CONTROL DEL AGENTE ---'));
    
    const { accion } = await inquirer.prompt([{
        type: 'list',
        name: 'accion',
        message: '¿Qué deseas hacer?',
        choices: [
            { name: '🔍 Analizar un archivo', value: 'leer' },
            { name: '📝 Modificar un archivo', value: 'escribir' },
            { name: '❌ Salir', value: 'salir' }
        ]
    }]);

    if (accion === 'salir') process.exit();

    const { nombreArchivo } = await inquirer.prompt([{
        type: 'input',
        name: 'nombreArchivo',
        message: 'Nombre del archivo (ej: package.json o test.txt):',
        default: 'package.json'
    }]);

    try {
        const contenido = await fs.readFile(nombreArchivo, 'utf-8');

        if (accion === 'leer') {
            const respuesta = await procesarConIA(`Explica brevemente qué hace este archivo y busca posibles errores:`, contenido);
            console.log(chalk.cyan('\nAnálisis:\n'), respuesta);
        } 
        else if (accion === 'escribir') {
            const { instruccion } = await inquirer.prompt([{
                type: 'input',
                name: 'instruccion',
                message: '¿Qué cambio quieres aplicar?:'
            }]);

            const nuevoContenido = await procesarConIA(instruccion, contenido);
            
            if (nuevoContenido) {
                await fs.writeFile(nombreArchivo, nuevoContenido);
                console.log(chalk.green(`\n✅ ¡Hecho! Archivo ${nombreArchivo} actualizado.`));
            }
        }
    } catch (err) {
        console.error(chalk.red('Error al acceder al archivo:'), err.message);
    }

    // Volver al menú (bucle infinito hasta salir)
    menuPrincipal();
}

menuPrincipal();
