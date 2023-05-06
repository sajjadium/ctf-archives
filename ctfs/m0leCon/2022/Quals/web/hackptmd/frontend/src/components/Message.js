function Message({ msg, type }) {
    if (!msg) {
        return <></>
    }

    return <>
        <div style={{ textAlign: 'center', width: '100%', marginTop: '10px' }}><span style={{ color: type === 'success' ? 'green' : 'red' }}>{type === 'success' ? 'Success: ' : 'Error: '}{msg}</span></div>
    </>
}

export { Message }
