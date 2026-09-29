import sys, json, re

class PersonalCommunicationTriageSentinel:
    """
    Personal Communication & Email Triage Sentinel.
    Evaluates inbound communications with VIP weighting, deadline detection,
    urgency classification, and auto-drafts contextual executive responses.
    """
    VIP_DOMAINS = {"fund.vc", "partner.co", "board.org", "keyclient.com"}
    URGENT_KEYWORDS = ["urgent", "asap", "deadline", "by today", "eod", "blocked", "action required"]

    def triage_message(self, message_id, sender, subject, body):
        is_vip = any(domain in sender.lower() for domain in self.VIP_DOMAINS)
        has_urgency = any(kw in (subject + " " + body).lower() for kw in self.URGENT_KEYWORDS)

        score = 50.0
        if is_vip: score += 30.0
        if has_urgency: score += 20.0
        if "unsubscribe" in body.lower(): score -= 40.0

        score = max(0.0, min(100.0, score))

        if score >= 80.0:
            tier = "URGENT_ACTION"
        elif score >= 50.0:
            tier = "NEEDS_REPLY"
        elif score >= 30.0:
            tier = "FYI_DIGEST"
        else:
            tier = "LOW_PRIORITY_NEWSLETTER"

        return {
            "message_id": message_id,
            "sender": sender,
            "subject": subject,
            "priority_score": score,
            "tier": tier,
            "is_vip": is_vip,
            "action_needed": tier in ("URGENT_ACTION", "NEEDS_REPLY")
        }

    def auto_draft_reply(self, message_info, user_tone="executive_concise"):
        sender_name = message_info.get("sender", "").split("@")[0].capitalize()
        subj = message_info.get("subject", "")
        
        reply = (
            f"Hi {sender_name},

"
            f"Thanks for reaching out regarding '{subj}'. I have reviewed the details and will follow up with the requested items by this afternoon.

"
            f"Best regards,
Alex"
        )
        return {"draft_reply": reply, "word_count": len(reply.split()), "tone_profile": user_tone}

    def generate_executive_digest(self, triaged_list):
        urgent = [m for m in triaged_list if m["tier"] == "URGENT_ACTION"]
        replies = [m for m in triaged_list if m["tier"] == "NEEDS_REPLY"]
        
        digest = (
            f"Inbox Briefing: You have {len(urgent)} urgent action items requiring immediate attention and "
            f"{len(replies)} communications queued for replies today."
        )
        return {"summary": digest, "urgent_count": len(urgent), "needs_reply_count": len(replies)}

    def run_communication_benchmark(self):
        sample_messages = [
            {"id": "m1", "sender": "sarah@fund.vc", "subject": "Urgent: Series A Term Sheet Signing", "body": "Please review and execute by EOD today."},
            {"id": "m2", "sender": "engineer@company.com", "subject": "Staging DB connection pool issue", "body": "Fixed in PR #104, please approve when free."},
            {"id": "m3", "sender": "newsletter@techdaily.com", "subject": "Top 10 AI frameworks this week", "body": "Click here to unsubscribe."}
        ]

        triaged = [self.triage_message(m["id"], m["sender"], m["subject"], m["body"]) for m in sample_messages]
        draft = self.auto_draft_reply(triaged[0])
        digest = self.generate_executive_digest(triaged)

        return {
            "suite": "Personal Communication Triage Sentinel Benchmark",
            "triaged_messages": triaged,
            "executive_digest": digest,
            "sample_auto_draft": draft,
            "inbox_state": "OPTIMAL_TRIAGE_ACTIVE"
        }
