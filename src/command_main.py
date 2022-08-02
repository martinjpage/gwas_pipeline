from src.view_models.project_view_model import ProjectViewModel


def command_main(id_term, name_term, user_project_folder, include_child):
    project = ProjectViewModel(user_project_folder)
    project.run(id_term, name_term, include_child)
