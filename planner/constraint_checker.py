def check_plan_constraints(plan):
    """
    Check whether the generated synthetic training plan
    satisfies the project's planning constraints.

    These are project-specific planning rules and are not
    medical recommendations.
    """

    violations = []

    previous_intensity = None

    for day in plan:

        date = day["date"]

        session = day["session"]

        # Normal training recommendations use "training_type".
        # Match sessions use "session_type".
        session_type = session.get(
            "session_type",
            session.get("training_type", "")
        )

        intensity = session.get(
            "intensity",
            ""
        )

        availability = day.get(
            "availability",
            "full"
        )

        is_match_day = day.get(
            "is_match_day",
            False
        )

        # ----------------------------------------
        # Constraint 1
        # Match day must contain MATCH
        # ----------------------------------------

        if is_match_day:

            if session_type != "MATCH":

                violations.append(
                    f"{date}: Match day does not contain a MATCH session."
                )

        # ----------------------------------------
        # Constraint 2
        # Limited availability should not receive
        # high-intensity training
        # ----------------------------------------

        if availability == "limited":

            if intensity == "high":

                violations.append(
                    f"{date}: High intensity conflicts with limited availability."
                )

        # ----------------------------------------
        # Constraint 3
        # No consecutive high-intensity sessions
        # ----------------------------------------

        if (
            intensity == "high"
            and previous_intensity == "high"
        ):

            violations.append(
                f"{date}: Consecutive high-intensity sessions."
            )

        previous_intensity = intensity

    return {
        "constraints_passed": len(violations) == 0,
        "violation_count": len(violations),
        "violations": violations
    }