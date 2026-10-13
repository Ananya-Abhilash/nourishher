import React, { useEffect, useState } from 'react'
import client, { apiError } from '../api/client'

const common = [
  'Fatigue',
  'Hair loss',
  'Headache',
  'Muscle weakness',
  'Dizziness',
  'Poor concentration',
  'Sleep problems',
  'Heavy periods',
  'Nausea',
]

const empty = {
  name: 'Fatigue',
  custom: '',
  severity: '3',
  frequency: 'occasional',
  start_date: '',
  notes: '',
}

export function SymptomsPage() {
  const [form, setForm] = useState(empty)
  const [items, setItems] = useState([])
  const [editing, setEditing] = useState(null)
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  const load = async () => {
    try {
      const { data } = await client.get('/symptoms/')
      setItems(Array.isArray(data) ? data : data.results || [])
    } catch (error) {
      setMessage(apiError(error))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const change = (key, value) => {
    setForm((previous) => ({
      ...previous,
      [key]: value,
    }))
  }

  const submit = async (event) => {
    event.preventDefault()
    setMessage('')

    const name =
      form.name === 'Other' ? form.custom.trim() : form.name

    if (!name) {
      setMessage('Enter a symptom name.')
      return
    }

    const payload = {
      name,
      severity: Number(form.severity),
      frequency: form.frequency,
      start_date: form.start_date || null,
      notes: form.notes,
    }

    setSaving(true)

    try {
      if (editing !== null) {
        await client.patch(`/symptoms/${editing}/`, payload)
      } else {
        await client.post('/symptoms/', payload)
      }

      setMessage('Symptom saved successfully.')
      setForm({ ...empty })
      setEditing(null)
      await load()
    } catch (error) {
      setMessage(apiError(error))
    } finally {
      setSaving(false)
    }
  }

  const edit = (item) => {
    const isCommon = common.includes(item.name)

    setEditing(item.id)
    setForm({
      name: isCommon ? item.name : 'Other',
      custom: isCommon ? '' : item.name,
      severity: String(item.severity),
      frequency: item.frequency,
      start_date: item.start_date || '',
      notes: item.notes || '',
    })

    setMessage('')
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const remove = async (id) => {
    if (!window.confirm('Delete this symptom entry?')) {
      return
    }

    setMessage('')

    try {
      await client.delete(`/symptoms/${id}/`)
      setItems((previous) => previous.filter((item) => item.id !== id))

      if (editing === id) {
        setEditing(null)
        setForm({ ...empty })
      }

      setMessage('Symptom deleted successfully.')
    } catch (error) {
      setMessage(apiError(error))
    }
  }

  return (
    <section className="labs-page">
      <p className="eyebrow">YOUR HEALTH RECORDS</p>
      <h1>Symptoms</h1>

      <p className="lead">
        Symptoms can have many causes and do not diagnose nutrient
        conditions.
      </p>

      <form className="form-card" onSubmit={submit}>
        <div className="result-grid">
          <label>
            Symptom
            <select
              value={form.name}
              onChange={(event) => change('name', event.target.value)}
            >
              {common.map((name) => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
              <option value="Other">Other</option>
            </select>
          </label>

          {form.name === 'Other' && (
            <label>
              Custom symptom
              <input
                required
                value={form.custom}
                onChange={(event) =>
                  change('custom', event.target.value)
                }
              />
            </label>
          )}

          <label>
            Severity
            <select
              value={form.severity}
              onChange={(event) =>
                change('severity', event.target.value)
              }
            >
              {[1, 2, 3, 4, 5].map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>
          </label>

          <label>
            Frequency
            <select
              value={form.frequency}
              onChange={(event) =>
                change('frequency', event.target.value)
              }
            >
              <option value="occasional">Occasional</option>
              <option value="daily">Daily</option>
              <option value="several_times_a_week">
                Several times a week
              </option>
              <option value="weekly">Weekly</option>
              <option value="unknown">Unknown</option>
            </select>
          </label>

          <label>
            Start date
            <input
              type="date"
              value={form.start_date}
              onChange={(event) =>
                change('start_date', event.target.value)
              }
            />
          </label>
        </div>

        <label>
          Notes
          <textarea
            value={form.notes}
            onChange={(event) => change('notes', event.target.value)}
          />
        </label>

        <button className="button" type="submit" disabled={saving}>
          {saving
            ? 'Saving...'
            : editing !== null
              ? 'Update symptom'
              : 'Save symptom'}
        </button>

        {editing !== null && (
          <button
            className="text-button"
            type="button"
            onClick={() => {
              setEditing(null)
              setForm({ ...empty })
              setMessage('')
            }}
          >
            Cancel edit
          </button>
        )}

        {message && <p role="status">{message}</p>}
      </form>

      <section className="report-history">
        <h2>Symptom history</h2>

        {loading ? (
          <p>Loading symptoms...</p>
        ) : items.length === 0 ? (
          <div className="empty-state">No symptoms recorded yet.</div>
        ) : (
          <div className="report-list">
            {items.map((item) => (
              <article className="report-card" key={item.id}>
                <div>
                  <h3>{item.name}</h3>
                  <p>
                    Severity {item.severity}/5 ·{' '}
                    {String(item.frequency).replaceAll('_', ' ')}
                  </p>

                  {item.start_date && <p>Started: {item.start_date}</p>}
                  {item.notes && <p>{item.notes}</p>}
                </div>

                <div>
                  <button
                    className="text-button"
                    type="button"
                    onClick={() => edit(item)}
                  >
                    Edit
                  </button>

                  <button
                    className="text-button"
                    type="button"
                    onClick={() => remove(item.id)}
                  >
                    Delete
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </section>
  )
}

export function AssessmentPage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let active = true

    const loadAssessment = async () => {
      try {
        const response = await client.get('/nutrients/assessment/')

        if (active) {
          setData(response.data)
          setError('')
        }
      } catch (err) {
        if (active) {
          setError(apiError(err))
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    loadAssessment()

    return () => {
      active = false
    }
  }, [])

  const results = Array.isArray(data?.results) ? data.results : []

  return (
    <section className="labs-page">
      <p className="eyebrow">TRANSPARENT ASSESSMENT</p>
      <h1>Nutrient Assessment</h1>

      <p className="lead">
        Preliminary observations based on your laboratory reference
        ranges. This is not a diagnosis.
      </p>

      {loading && <p>Loading assessment...</p>}

      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}

      {!loading && !error && data && (
        <>
          {results.length === 0 ? (
            <div className="empty-state">
              No assessment results are available yet. Add blood-test
              results with laboratory reference ranges to get started.
            </div>
          ) : (
            <div className="report-list">
              {results.map((result, index) => {
                const evidence = Array.isArray(result.evidence)
                  ? result.evidence
                  : []

                const limitations = Array.isArray(result.limitations)
                  ? result.limitations
                  : []

                return (
                  <article
                    className="form-card"
                    key={`${result.nutrient || 'nutrient'}-${index}`}
                  >
                    <h2>{result.nutrient || 'Nutrient assessment'}</h2>

                    <p>
                      <strong>
                        {String(result.status || 'insufficient_data')
                          .replaceAll('_', ' ')}
                      </strong>
                    </p>

                    {evidence.length > 0 ? (
                      evidence.map((item, evidenceIndex) => (
                        <p key={evidenceIndex}>
                          {item.biomarker || 'Lab result'}:{' '}
                          {item.value ?? '—'} {item.unit || ''}
                          {' · Reference range: '}
                          {item.reference_low ?? '—'} –{' '}
                          {item.reference_high ?? '—'}
                          {item.test_date
                            ? ` · Date: ${item.test_date}`
                            : ''}
                        </p>
                      ))
                    ) : (
                      <p>No relevant lab evidence is available.</p>
                    )}

                    {limitations.length > 0 && (
                      <ul>
                        {limitations.map((item, limitationIndex) => (
                          <li key={limitationIndex}>{item}</li>
                        ))}
                      </ul>
                    )}
                  </article>
                )
              })}
            </div>
          )}

          <p className="lead">
            These observations are not a medical diagnosis. Discuss
            concerns about your results with a qualified healthcare
            professional.
          </p>
        </>
      )}
    </section>
  )
}