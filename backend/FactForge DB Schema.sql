CREATE TABLE "queries" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "question" text NOT NULL,
  "status" varchar(50) NOT NULL DEFAULT 'queued',
  "created_at" timestamp NOT NULL DEFAULT (now())
);

CREATE TABLE "sub_questions" (
  "id" uuid PRIMARY KEY,
  "query_id" uuid NOT NULL,
  "text" text NOT NULL
);

CREATE TABLE "sources" (
  "id" uuid PRIMARY KEY,
  "sub_question_id" uuid NOT NULL,
  "url" text NOT NULL,
  "domain" varchar(255) NOT NULL,
  "title" text,
  "published_at" timestamp,
  "fetched_at" timestamp NOT NULL DEFAULT (now()),
  "is_independent" boolean NOT NULL DEFAULT false
);

CREATE TABLE "claims" (
  "id" uuid PRIMARY KEY,
  "sub_question_id" uuid NOT NULL,
  "text" text NOT NULL,
  "verification_status" varchar(50) NOT NULL DEFAULT 'pending',
  "confidence_score" decimal(5,4),
  "retry_count" integer NOT NULL DEFAULT 0,
  "is_unresolved" boolean NOT NULL DEFAULT false
);

CREATE TABLE "claim_sources" (
  "claim_id" uuid NOT NULL,
  "source_id" uuid NOT NULL,
  "relation" varchar(20) NOT NULL,
  PRIMARY KEY ("claim_id", "source_id")
);

CREATE TABLE "reports" (
  "id" uuid PRIMARY KEY,
  "query_id" uuid NOT NULL,
  "final_text" text NOT NULL,
  "generated_at" timestamp NOT NULL DEFAULT (now())
);

CREATE TABLE "feedback" (
  "id" uuid PRIMARY KEY,
  "claim_id" uuid NOT NULL,
  "user_id" uuid NOT NULL,
  "flag_reason" text NOT NULL,
  "created_at" timestamp NOT NULL DEFAULT (now())
);

ALTER TABLE "sub_questions" ADD FOREIGN KEY ("query_id") REFERENCES "queries" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "sources" ADD FOREIGN KEY ("sub_question_id") REFERENCES "sub_questions" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "claims" ADD FOREIGN KEY ("sub_question_id") REFERENCES "sub_questions" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "claim_sources" ADD FOREIGN KEY ("claim_id") REFERENCES "claims" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "claim_sources" ADD FOREIGN KEY ("source_id") REFERENCES "sources" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "reports" ADD FOREIGN KEY ("query_id") REFERENCES "queries" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "feedback" ADD FOREIGN KEY ("claim_id") REFERENCES "claims" ("id") DEFERRABLE INITIALLY IMMEDIATE;
