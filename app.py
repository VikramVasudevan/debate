from dotenv import load_dotenv
import gradio as gr
from src.debate.crew import Debate

PROPOSITION_DEFAULT = "### Arguments in favor\n\n_Arguments in favor will appear here_"
OPPOSITION_DEFAULT = "### Arguments against\n\n_Arguments against will appear here_"
DECISION_DEFAULT = "### The Judge's Decision\n\n_Decision will appear here_"

def debate_motion(motion):
    debate = Debate()
    crew = debate.crew()
    inputs = {
        'motion': motion
    }
    results = crew.kickoff(inputs=inputs)
    print("Results: ", results)
    proposition = debate.my_proposition_task.output.raw
    opposition = debate.my_opposition_task.output.raw
    decision = debate.my_judge_task.output.raw

    yield proposition, opposition, decision


if __name__ == "__main__":
    load_dotenv(override=True)
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        motion = gr.Text(
            label="Motion",
            value="Being Vegan is better for the environment",
            submit_btn="Start Debate",
            placeholder="Enter a motion to debate",
        )

        with gr.Column():
            with gr.Row(equal_height=True):
                proposition = gr.Markdown(
                    value=PROPOSITION_DEFAULT,
                    container=True,
                )

                opposition = gr.Markdown(
                    value=OPPOSITION_DEFAULT,
                    container=True,
                )

            decision = gr.Markdown(
                value=DECISION_DEFAULT,
                container=True,
            )

        motion.submit(
            debate_motion, inputs=[motion], outputs=[proposition, opposition, decision]
        )
    demo.launch()
