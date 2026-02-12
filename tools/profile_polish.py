#!/usr/bin/env python3
import argparse
import json
import sys

def generate_short_bio(niche, skills):
    skill_list = [s.strip() for s in skills.split(',')]
    top_skills = ", ".join(skill_list[:3])
    return f"Specialist in {niche}. Expert in {top_skills}. Building high-impact solutions."

def generate_long_bio(bio, niche, skills, proof):
    skill_list = [s.strip() for s in skills.split(',')]
    return (
        f"I help clients in the {niche} space achieve their goals through {', '.join(skill_list[:4])}. "
        f"With a track record including {proof}, I focus on delivering measurable results. "
        f"{bio}"
    )

def generate_pinned_post(niche, proof, skills):
    return (
        f"🚀 OPEN FOR WORK: {niche.upper()} SPECIALIST\n\n"
        f"I'm currently taking on new projects in {niche}.\n\n"
        f"Why work with me?\n"
        f"✅ Proven results: {proof}\n"
        f"✅ Core stack: {skills}\n\n"
        "DM me to discuss your project. Let's build something great."
    )

def generate_keywords(niche, skills):
    base_keywords = [k.strip() for k in skills.split(',')]
    niche_keywords = [niche, f"{niche} Expert", f"{niche} Developer", "Freelancer", "Remote"]
    all_keywords = base_keywords + niche_keywords
    # Deduplicate and limit to 10
    unique_keywords = list(dict.fromkeys(all_keywords))
    return unique_keywords[:10]

def generate_bullets(proof, skills):
    # This is a simple heuristic generator
    bullets = [
        f"Specialized focus on {skills.split(',')[0]}",
        f"Proven track record in {proof.split('.')[0] if '.' in proof else proof}",
        "Deliverable-focused workflow",
        "Clear communication & timely updates",
        "Post-launch support available"
    ]
    return bullets

def main():
    parser = argparse.ArgumentParser(description="Profile Polish: Generate optimized profile content.")
    parser.add_argument("--bio", required=True, help="Current bio text")
    parser.add_argument("--skills", required=True, help="Comma-separated list of skills")
    parser.add_argument("--niche", required=True, help="Target niche/industry")
    parser.add_argument("--proof", required=True, help="Key proof points or achievements")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    short_bio = generate_short_bio(args.niche, args.skills)
    long_bio = generate_long_bio(args.bio, args.niche, args.skills, args.proof)
    pinned_post = generate_pinned_post(args.niche, args.proof, args.skills)
    keywords = generate_keywords(args.niche, args.skills)
    bullets = generate_bullets(args.proof, args.skills)

    data = {
        "short_bio": short_bio,
        "long_bio": long_bio,
        "pinned_post": pinned_post,
        "keywords": keywords,
        "credibility_bullets": bullets
    }

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print("=== PROFILE POLISH OUTPUT (PD BRAND) ===")
        print("\n--- SHORT BIO ---")
        print(short_bio)
        print("\n--- LONG BIO ---")
        print(long_bio)
        print("\n--- PINNED POST ---")
        print(pinned_post)
        print("\n--- 10 KEYWORDS ---")
        print(", ".join(keywords))
        print("\n--- 5 CREDIBILITY BULLETS ---")
        for b in bullets:
            print(f"- {b}")

if __name__ == "__main__":
    main()
