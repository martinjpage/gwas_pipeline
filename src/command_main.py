from src.view_models.project_view_model import ProjectViewModel


def command_main(id_term, name_term, user_project_folder):
    # ToDo - add mtag file path and column names for variant and chromosome into config
    project = ProjectViewModel(user_project_folder)
    project.run(id_term, name_term)
