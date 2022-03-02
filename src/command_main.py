from src.view_models.project_view_model import ProjectViewModel


def command_main(id_term, name_term, output_path):
    project = ProjectViewModel()
    project.run(id_term, name_term, output_path)
