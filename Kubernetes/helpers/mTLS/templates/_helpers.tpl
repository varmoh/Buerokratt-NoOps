{{/* Define a helper function to generate the full name */}}
{{- define "mTLS.fullname" -}}
{{- $name := printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- $name | replace "_" "-" | replace "." "-" | lower -}}
{{- end }}
