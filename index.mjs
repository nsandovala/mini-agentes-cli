import ollama from 'ollama';
import chalk from 'chalk';
import ora from 'ora';
import fs from 'fs/promises';

async function ejecutarAgente() {
  const archivo = 'test.txt'; 
  // Creamos un archivo de prueba para no romper nada
  await fs.writeFile(archivo, "Hola, este es un archivo de prueba.");

  console.log(chalk.blue.bold('\n🚀 Agente Escritor Activo'));
  
  const pregunta = "Agrega una línea al final del archivo que diga 'Modificado por Qwen'";
  const spinner = ora('El modelo está decidiendo cómo editar...').start();

  try {
    const contenidoActual = await fs.readFile(archivo, 'utf-8');

    const response = await ollama.chat({
      model: 'qwen3-coder', // Cambia al nombre exacto que tengas en Ollama
      messages: [
        { 
          role: 'system', 
          content: `Eres un agente que edita archivos. 
          Para editar, debes responder ÚNICAMENTE con el nuevo contenido completo del archivo. 
          No des explicaciones, solo el código/texto.` 
        },
        { 
          role: 'user', 
          content: `Archivo actual:\n${contenidoActual}\n\nInstrucción: ${pregunta}` 
        },
      ],
    });

    const nuevoContenido = response.message.content.trim();
    
    // El Agente aplica el cambio físicamente
    await fs.writeFile(archivo, nuevoContenido);
    
    spinner.stop();
    console.log(chalk.green(`\n✅ Archivo '${archivo}' actualizado con éxito.`));
    console.log(chalk.dim(`Contenido final:\n"${nuevoContenido}"`));

  } catch (error) {
    spinner.stop();
    console.error(chalk.red('Error:'), error.message);
  }
}

ejecutarAgente();
