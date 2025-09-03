{{/*
Create the name of the chart: ReleaseName or nameOverride
*/}}
{{- define "aapb.name" -}}
{{- default .Release.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create the frontend name: ReleaseName-frontendName
*/}}
{{- define "aapb.frontend.fullname" -}}
{{- printf "%s-%s" (include "aapb.name" .) .Values.global.frontend.name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create the frontend url: ReleaseName.host
*/}}
{{- define "aapb.url" -}}
{{- if .Values.global.url -}}
{{- .Values.global.url -}}
{{- else -}}
{{- printf "%s.%s" (include "aapb.name" .) .Values.global.host -}}
{{- end -}}
{{- end -}}
