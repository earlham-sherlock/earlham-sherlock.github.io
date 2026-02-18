#!/usr/bin/env bash


# removing the optional 's3a://', 's3://', BUCKET_NAME, or '/' from the beginning of the BACKUP NAME
BACKUP_PATH=${BACKUP_PATH#"s3a://"}
BACKUP_PATH=${BACKUP_PATH#"s3://"}
BACKUP_PATH=${BACKUP_PATH#"${S3_BUCKET}/"}
BACKUP_PATH=${BACKUP_PATH#"/"}

# remove protocol prefix from endpoint url
S3_END_POINT=${S3_END_POINT#"http://"}
S3_END_POINT=${S3_END_POINT#"https://"}

# DigitalOcean Spaces endpoints are typically "<region>.digitaloceanspaces.com".
# Users sometimes provide "<bucket>.<region>.digitaloceanspaces.com"; normalize that.
if [[ -n "${S3_BUCKET:-}" && "${S3_END_POINT}" == "${S3_BUCKET}."* ]]; then
	S3_END_POINT="${S3_END_POINT#"${S3_BUCKET}."}"
fi

# s3cmd needs a proper host_bucket template and region (bucket_location) for v4 signing.
# - Path-style:  host_bucket = endpoint/%(bucket)
# - VHost-style: host_bucket = %(bucket).endpoint
if [[ "${S3_PATH_STYLE_ACCESS:-true}" == "true" ]]; then
	export S3_HOST_BUCKET="${S3_END_POINT}/%(bucket)"
else
	export S3_HOST_BUCKET="%(bucket).${S3_END_POINT}"
fi

# Default region/bucket_location handling (important for DigitalOcean Spaces and AWS).
if [[ -z "${S3_REGION:-}" ]]; then
	if [[ "${S3_END_POINT}" == *.digitaloceanspaces.com ]]; then
		# "ams3.digitaloceanspaces.com" -> "ams3"
		export S3_REGION="${S3_END_POINT%%.*}"
	elif [[ "${S3_END_POINT}" == s3.*.amazonaws.com ]]; then
		tmp="${S3_END_POINT#s3.}"
		export S3_REGION="${tmp%%.amazonaws.com}"
	else
		export S3_REGION="us-east-1"
	fi
fi

echo "generating ~/.s3cfg"
envsubst < /s3cfg_template > ~/.s3cfg


$@