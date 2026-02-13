import React from 'react';
import './Modal.css';

const Modal = ({ isOpen, onClose, title, children, onConfirm, confirmText = "Confirm", cancelText = "Cancel", isDanger = false }) => {
    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
                <div className="modal-header">
                    {title}
                </div>
                <div className="modal-body">
                    {children}
                </div>
                <div className="modal-footer">
                    <button className="modal-btn cancel-btn" onClick={onClose}>
                        {cancelText}
                    </button>
                    <button
                        className={`modal-btn ${isDanger ? 'confirm-btn' : 'primary-btn'}`}
                        onClick={() => {
                            onConfirm();
                            onClose();
                        }}
                    >
                        {confirmText}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Modal;
