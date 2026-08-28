from utils.sql import supabase


def build_database_context():
    """
    Fetches team, project, and daily update data
    and converts it into readable context for the LLM.
    """

    members_resp = (
        supabase
        .table("team_members")
        .select("*")
        .execute()
    )

    projects_resp = (
        supabase
        .table("projects")
        .select("*")
        .execute()
    )

    updates_resp = (
        supabase
        .table("daily_updates")
        .select("*")
        .execute()
    )

    team_members = members_resp.data or []
    projects = projects_resp.data or []
    updates = updates_resp.data or []

    member_lookup = {
        member["id"]: member["full_name"]
        for member in team_members
    }

    project_lookup = {
        project["id"]: project["project_name"]
        for project in projects
    }

    # -----------------------------
    # Team Members
    # -----------------------------

    member_context = "\n".join(
        [
            f"""
Name: {member.get('full_name', 'Unknown')}
Role: {member.get('role', 'Unknown')}
Department: {member.get('department', 'Unknown')}
Email: {member.get('email', 'Unknown')}
"""
            for member in team_members
        ]
    )

    # -----------------------------
    # Projects
    # -----------------------------

    project_context = "\n".join(
        [
            f"""
Project: {project.get('project_name', 'Unknown')}
Status: {project.get('status', 'Unknown')}
Description: {project.get('description', 'No description available')}
"""
            for project in projects
        ]
    )

    # -----------------------------
    # Daily Updates
    # -----------------------------

    formatted_updates = []

    for update in updates:

        member_name = member_lookup.get(
            update.get("member_id"),
            "Unknown Member"
        )

        project_name = project_lookup.get(
            update.get("project_id"),
            "Unknown Project"
        )

        blockers = update.get("blockers")

        if (
            blockers is None
            or str(blockers).strip().lower()
            in ["", "no", "none", "nil"]
        ):
            blockers = "No blockers reported"

        formatted_updates.append(
            f"""
Team Member: {member_name}

Project: {project_name}

Date: {update.get('update_date', 'Unknown')}

Task Completed:
{update.get('task_completed', 'No task description')}

Hours Worked:
{update.get('hours_worked', 0)}

Current Status:
{update.get('status', 'Unknown')}

Blockers:
{blockers}
"""
        )

    updates_context = (
        "\n----------------------------------------\n"
        .join(formatted_updates)
    )

    return f"""
================ TEAM MEMBERS ================

{member_context}

================ PROJECTS ====================

{project_context}

================ DAILY UPDATES ===============

{updates_context}
"""