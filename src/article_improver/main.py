import typer
from article_improver import config
from article_improver.chat_gpt import ChatGpt
from article_improver.command import config_command, seo
from openai import AsyncOpenAI
from rich.progress import Progress, SpinnerColumn, TextColumn

app = typer.Typer()
cfg, loop = config.init()

if cfg is not None:
    chat_gpt = ChatGpt(AsyncOpenAI(api_key=cfg.open_ai_key))


def execute_chat_gpt_command(description, fn):
    if cfg is None:
        configure_command()
        print("Run command again.")
        
    else:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description=description, total=None)
            loop.run_until_complete(fn())


@app.command(name="seo")
def seo_command(filename: str):
    async def cmd():
        await seo.handle(chat_gpt, filename)

    execute_chat_gpt_command("Generating seo recommendations!", cmd)


@app.command(name="configure")
def configure_command():
    config_command.handle(config.DEFAULT_CONFIG_FILE, config.DEFAULT_CONFIG_FILE_FOLDER)


if __name__ == "__main__":
    app()
